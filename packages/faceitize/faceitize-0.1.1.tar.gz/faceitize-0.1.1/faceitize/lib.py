import dlib
import cv2
import requests
import numpy as np
from skimage import io

FACE_DETECTOR = dlib.get_frontal_face_detector()
LANDMARK_PREDICTOR = dlib.shape_predictor()


def replace_faces(img,
                  src_img,
                  src_points,
                  detector=FACE_DETECTOR,
                  landmark_predictor=LANDMARK_PREDICTOR):
    """Replaces all faces in an image, uses pointers"""
    faces = detector(img, 1)

    for face in faces:
        img = replace_face(
            img,
            face,
            src_img,
            src_points,
            landmark_predictor=landmark_predictor)

    return img


def replace_face(img,
                 face_box,
                 src_img,
                 src_points,
                 landmark_predictor=LANDMARK_PREDICTOR):
    """Replaces a single face in the given coordinates """
    img_copy = np.copy(img)
    landmarks = landmarks_to_tpl(landmark_predictor(img, face_box))
    bound_box = cv2.boundingRect(np.float32([landmarks]))
    face_shape = [i[0] for i in cv2.convexHull(np.float32(landmarks))]

    # Create a subdiv for calculating delauney triangles
    subdiv = get_subdiv(landmarks)

    # Warp delanuey triangulation from src to target image
    triangles = calc_delauney_triangles(subdiv, landmarks)
    for tri in triangles:
        tri1 = []
        tri2 = []
        try:
            for point in tri:
                tri1.append(landmarks[point])
                tri2.append(src_points[point])

            warp_triangle(src_img, img, tri2, tri1)
        except Exception:
            continue

    # Finally blend the images together, this makes the new image look
    # more natural
    return blend_img(img, img_copy, face_shape)


def blend_img(img, target, shape):
    mask = np.zeros(img.shape, dtype=img.dtype)
    bound_box = cv2.boundingRect(np.float32([shape]))
    center = ((bound_box[0] + int(bound_box[2] / 2),
               bound_box[1] + int(bound_box[3] / 2)))

    cv2.fillConvexPoly(mask, np.int32([shape]), (255, 255, 255))
    return cv2.seamlessClone(
        np.uint8(img), target, mask, center, cv2.NORMAL_CLONE)


#calculate delanauy triangle
def calc_delauney_triangles(subdiv, points):
    triangleList = subdiv.getTriangleList()
    delaunayTri = []
    pt = []
    count = 0

    for t in triangleList:
        pt = [(t[0], t[1]), (t[2], t[3]), (t[4], t[5])]

        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

        count = count + 1
        ind = []
        for j in range(0, 3):
            for k in range(0, len(points)):
                if (abs(pt[j][0] - points[k][0]) < 1.0
                        and abs(pt[j][1] - points[k][1]) < 1.0):
                    ind.append(k)
        if len(ind) == 3:
            delaunayTri.append((ind[0], ind[1], ind[2]))

        pt = []

    return delaunayTri


# Apply affine transform calculated using srcTri and dstTri to src and
# output an image of size.
def applyAffineTransform(src, srcTri, dstTri, size):

    # Given a pair of triangles, find the affine transform.
    warpMat = cv2.getAffineTransform(np.float32(srcTri), np.float32(dstTri))

    # Apply the Affine Transform just found to the src image
    dst = cv2.warpAffine(
        src,
        warpMat, (size[0], size[1]),
        None,
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_REFLECT_101)

    return dst


# Warps and alpha blends triangular regions from img1 and img2 to img
def warp_triangle(img1, img2, t1, t2):
    # Find bounding rectangle for each triangle
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))

    # Offset points by left top corner of the respective rectangles
    t1Rect = []
    t2Rect = []
    t2RectInt = []

    for i in range(0, 3):
        t1Rect.append(((t1[i][0] - r1[0]), (t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))
        t2RectInt.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))

    # Get mask by filling triangle
    mask = np.zeros((r2[3], r2[2], 3), dtype=np.float32)
    cv2.fillConvexPoly(mask, np.int32(t2RectInt), (1.0, 1.0, 1.0), 16, 0)

    # Apply warpImage to small rectangular patches
    img1Rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]

    size = (r2[2], r2[3])

    img2Rect = applyAffineTransform(img1Rect, t1Rect, t2Rect, size)

    img2Rect = img2Rect * mask

    # Copy triangular region of the rectangular patch to the output image
    img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] = img2[r2[
        1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] * ((1.0, 1.0, 1.0) - mask)

    img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] +
         r2[2]] = img2[r2[1]:r2[1] + r2[3], r2[0]:r2[0] + r2[2]] + img2Rect


def get_subdiv(landmarks):
    subdivision = cv2.Subdiv2D(cv2.boundingRect(np.float32([landmarks])))
    for i in landmarks:
        try:
            subdivision.insert(i)
        except Exception:
            return False

    return subdivision


def get_convex_index(points):
    return cv2.convexHull(points, returnPoints=False)


def landmarks_to_arr(landmarks):
    return np.array(
        [(landmarks.part(i).x, landmarks.part(i).y) for i in range(0, 67)])


def landmarks_to_tpl(landmarks):
    return [(landmarks.part(i).x, landmarks.part(i).y) for i in range(0, 67)]
