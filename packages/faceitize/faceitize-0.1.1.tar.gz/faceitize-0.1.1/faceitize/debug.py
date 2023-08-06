import cv2

# Debug function for asserting the dejauney calculation is working
def draw_delauney(img, subdiv):
    delaunay_color = (255, 255, 255)
    triangles = subdiv.getTriangleList()
    t_size = img.shape
    r = (0, 0, t_size[1], t_size[0])

    for triangle in triangles:

        # (x, y)
        pt1 = (triangle[0], triangle[1])
        pt2 = (triangle[2], triangle[3])
        pt3 = (triangle[4], triangle[5])

        if rect_contains(r, pt1) and rect_contains(r, pt2) and rect_contains(
                r, pt3):
            cv2.line(img, pt1, pt2, delaunay_color, 1, cv2.LINE_AA, 0)
            cv2.line(img, pt2, pt3, delaunay_color, 1, cv2.LINE_AA, 0)
            cv2.line(img, pt3, pt1, delaunay_color, 1, cv2.LINE_AA, 0)
    return img

def draw_rect(img, rect):
    delaunay_color = (255, 255, 255)
    cv2.line(img, (rect[0], rect[1]), (rect[0], rect[3]), delaunay_color, 1, cv2.LINE_AA, 0)
    cv2.line(img, (rect[0], rect[3]), (rect[2], rect[3]), delaunay_color, 1, cv2.LINE_AA, 0)
    cv2.line(img, (rect[2], rect[3]), (rect[2], rect[1]), delaunay_color, 1, cv2.LINE_AA, 0)
    cv2.line(img, (rect[2], rect[1]), (rect[0], rect[1]), delaunay_color, 1, cv2.LINE_AA, 0)

# Check if a point is inside a rectangle
def rect_contains(rect, point):
    if point[0] < rect[0]:
        return False
    elif point[1] < rect[1]:
        return False
    elif point[0] > rect[2]:
        return False
    elif point[1] > rect[3]:
        return False
    return True
