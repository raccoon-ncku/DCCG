from compas.geometry import Box, Frame

def running_bond_wall(length, height, brick=(0.24, 0.115, 0.06), joint=0.01):
    """
    Builds a running bond wall along the x-axis.
    
    Args:
        length: Total length of the wall along x.
        height: Total height of the wall along z.
        brick: Tuple of (length, depth, height) for a single brick.
        joint: Width of the mortar joint.
        
    Returns:
        A list of compas.geometry.Box objects.
    """
    b_len, b_dep, b_hgt = brick
    course_h = b_hgt + joint
    
    bricks = []
    
    # Calculate number of courses that fit within the height
    num_courses = int(height // course_h)
    
    for c in range(num_courses):
        # Calculate the x-offset for the running bond pattern
        # Even courses (0, 2...) start at 0. 
        # Odd courses (1, 3...) are offset by half a module (brick + joint)
        module = b_len + joint
        offset = 0.0
        if c % 2 == 1:
            offset = module / 2.0
            
        # Current course z-center: 
        # The bottom of the first course is at z=0.
        # The center of the first course is at z = b_hgt/2.
        # Subsequent courses are spaced by course_h.
        z_center = (c * course_h) + (b_hgt / 2.0)
        
        # We need to find how many bricks fit in this course given the offset.
        # We iterate through possible brick positions starting from the offset.
        # Because the wall must stay within [0, length], we check the bounds.
        
        # To handle the offset correctly and ensure we don't miss bricks that 
        # might start "before" 0 but are part of the pattern, we check 
        # positions starting from the offset and also check the "negative" side 
        # if the offset pushes the first brick into the wall.
        
        # However, the spec says "as many full bricks as fit within length" 
        # and "No brick may stick out past [0, length]".
        # This implies we start placing bricks at the offset and check if they fit.
        # If the offset is 0, we start at 0. If offset is > 0, we start at 0 
        # but the pattern is shifted.
        
        # Let's find the first valid x-position for a brick in this course.
        # A brick's left edge is x_start. x_start must be >= 0.
        # The pattern is: x_start = offset + k * module.
        # We need to find k such that offset + k * module >= 0.
        
        # Start with k = 0, but if offset is positive, we might need to check 
        # if a brick starting at (offset - module) fits.
        # But the spec says "each course is offset from the one below by half a module".
        # This implies the pattern is fixed.
        
        # Let's find the smallest k such that (offset + k * module) >= 0.
        # Since offset is either 0 or module/2, k=0 is the smallest non-negative.
        # If offset is module/2, we check if (offset - module) is a valid start.
        # (offset - module) = -module/2. This would stick out past 0.
        # So we only consider k >= 0 such that offset + k*module >= 0.
        
        # Actually, the simplest way to implement "offset" is to treat the 
        # pattern as x = offset + k * module, and only keep bricks where 
        # 0 <= x_start and x_end <= length.
        
        # However, if offset is module/2, the first brick in the pattern 
        # might be at x = -module/2 (invalid) or x = module/2 (valid).
        # We must check both the "shifted" start and the "standard" start 
        # to ensure we fill the length correctly.
        
        # Let's try k values that could result in a brick within [0, length].
        # The possible x_starts are: ... offset-module, offset, offset+module ...
        # We find the smallest k such that offset + k*module >= 0.
        
        k = 0
        if offset > 0:
            # If offset is module/2, then offset - module is -module/2.
            # We check if that brick fits. It won't (it's < 0).
            # So we start with k=0.
            pass
            
        current_x = offset
        # If the offset is positive, we should also check if the brick 
        # that would have been at (offset - module) could be shifted to 
        # fit? No, the offset is a fixed property of the course.
        
        # To ensure we don't miss a brick that starts at 0 due to the offset:
        # If offset is module/2, the brick at x = -module/2 is invalid.
        # The next brick is at x = module/2.
        # But wait, if the offset is module/2, the brick at x = -module/2 
        # is the "half-brick" in a running bond. But the spec says 
        # "as many full bricks as fit".
        
        # Let's refine:
        # A brick is valid if 0 <= x_start and x_start + b_len <= length.
        # The sequence of x_starts is: offset + k * module.
        # We need to find all k such that 0 <= offset + k*module and offset + k*module + b_len <= length.
        
        # Since offset is 0 or module/2:
        # If offset = 0: k = 0, 1, 2...
        # If offset = module/2: k = 0, 1, 2... (because k=-1 gives x_start = -module/2)
        
        # Wait, if offset = module/2, the brick at x = -module/2 is invalid.
        # But what if the brick at x = module/2 is the first one? 
        # That's what k=0 gives.
        
        # Let's check if we can start at a different k to get closer to 0.
        # If offset = module/2, k=0 -> x_start = module/2.
        # If we used k=-1, x_start = -module/2 (invalid).
        # So k=0 is the first valid k.
        
        # However, there is a catch: if the offset is module/2, the "running bond" 
        # pattern usually implies the bricks are shifted. 
        # If we only use k=0, 1, 2..., we are starting the bricks at module/2.
        # This is correct.
        
        # One edge case: what if the offset is module/2, but the brick 
        # at x = -module/2 + module/2 = 0? 
        # That would happen if the offset was 0.
        # The spec says "each course is offset from the one below by half a module".
        # This means if course 0 starts at 0, course 1 starts at module/2.
        
        # Let's try to find the smallest k such that offset + k*module >= 0.
        # Since offset is 0 or module/2, k=0 is always the smallest non-negative.
        # But we should check if k=-1 is possible? 
        # If offset = module/2, k=-1 => x_start = -module/2 (invalid).
        # So k=0 is the first.
        
        # BUT, what if the offset is such that a brick could start at 0?
        # If offset = module/2, the bricks are at module/2, 3/2 module, etc.
        # If offset = 0, the bricks are at 0, module, 2*module, etc.
        # This satisfies the "vertical joints never align" rule.
        
        # Let's check if we can shift the whole course to the left to fit more bricks?
        # No, the offset is relative to the course below.
        
        # Let's try to find the first k such that offset + k*module >= 0.
        # Since offset is 0 or module/2, k=0 is the first.
        # But we must also check if we can shift the pattern to the left 
        # while maintaining the offset? No, the offset is the shift.
        
        # Let's re-read: "each course is offset from the one below by half a module".
        # This means if course 0 has bricks at x = 0, m, 2m...
        # Course 1 has bricks at x = m/2, 3m/2, 5m/2...
        # Course 2 has bricks at x = 0, m, 2m...
        
        # This logic works. Let's implement it.
        
        # We need to find the starting k.
        # If offset is 0, k_start = 0.
        # If offset is module/2, k_start = 0.
        # Wait, if offset is module/2, the bricks are at m/2, 3m/2...
        # Is it possible to have a brick at x=0 in the offset course?
        # Only if the offset was 0.
        
        # Let's check if we can start at a negative k to get a brick at x=0?
        # If offset = m/2, k=-1 => x_start = -m/2. (Invalid)
        # So k=0 is the first valid k.
        
        # However, there's a subtle point: if the offset is m/2, 
        # the bricks are at m/2, 3m/2... 
        # But what if the bricks were at -m/2, m/2, 3m/2... 
        # The brick at -m/2 is invalid. The brick at m/2 is valid.
        # This is exactly what k=0, 1, 2... does.
        
        # One more thing: what if the offset is m/2, but we could fit a brick 
        # starting at 0? That would only happen if the offset was 0.
        # So the logic is:
        # x_start = offset + k * module
        # We want all k such that 0 <= x_start and x_start + b_len <= length.
        
        # To find the range of k:
        # 1. offset + k*module >= 0  =>  k >= -offset/module
        # 2. offset + k*module + b_len <= length => k <= (length - b_len - offset) / module
        
        import math
        k_min = math.ceil(-offset / module)
        k_max = math.floor((length - b_len - offset) / module)
        
        for k in range(k_min, k_max + 1):
            x_start = offset + k * module
            x_center = x_start + b_len / 2.0
            y_center = b_dep / 2.0
            z_center = z_center # already calculated
            
            # Create the frame for the box
            # Frame(point, x_axis, y_axis)
            # The box is centered on the frame.
            # The box dimensions are (b_len, b_dep, b_hgt).
            # The box is aligned with the axes.
            f = Frame([x_center, y_center, z_center], [1, 0, 0], [0, 1, 0])
            bricks.append(Box(b_len, b_dep, b_hgt, frame=f))
            
    return bricks
