#unit ; cm

side = 5
width = .2
#length

def su_polygon(*pts)
  lns = []
  last_pt = None;
  pts.append(pts[0])
  for pt in pts:
    if last_pt != None:
      lns.append(ln(last_pt, pt))
          
  return su(lns)

pt_origin = pt(0, 0, 0)
pt_sqr1_two = pt(pt_origin, va_side, 0, 0)
pt_sqr1_tree = pt(pt_sqr1_two, 0, va_side, 0)
pt_sqr1_four = pt(pt_sqr1_tree, -va_side, 0 , 0)

su_sqr1 = su_polygon(pt_origin, pt_sqr1_two, pt_sqr1_tree, pt_sqr1_four)

pt_sqr2_one = pt(va_width, va_width, 0)
pt_sqr2_two = pt(pt_sqr2_one, va_side - 2 * va_width, 0, 0)
pt_sqr2_tree = pt(pt_sqr2_two, 0, va_side - 2 * va_width, 0)
pt_sqr2_four = pt(pt_sqr2_tree, -va_side + 2 * va_width, 0 , 0)

su_sqr_2 = su_polygon(pt_sqr2_one, pt_sqr2_two, pt_sqr2_tree, pt_sqr2_four)

su_section = su_sqr_1 - su_sqr_2

vo_pipe = vo_extrusion(su_section, 20*ve_z)