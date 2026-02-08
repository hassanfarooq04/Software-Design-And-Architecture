def calculate_rectangle_area(length: float, width: float) -> float:
    """
    Calculate the area of a rectangle.

    This function takes the length and width of a rectangle and returns its area.

    Parameters:
        length (float): The length of the rectangle.
        width (float): The width of the rectangle.

    Returns:
        float: The calculated area of the rectangle.
    """
    # The formula for the area of a rectangle is length * width. This is an inline comment.
    area = length * width 
    return area  # Return the calculated area.

# Example usage with inline comment explaining the call
rect_length = 10.5  # Length of the rectangle
rect_width = 7.2   # Width of the rectangle

# Call the function to find the area
my_area = calculate_rectangle_area(rect_length, rect_width)

print(f"The area of the rectangle with length {rect_length} and width {rect_width} is {my_area}.")
