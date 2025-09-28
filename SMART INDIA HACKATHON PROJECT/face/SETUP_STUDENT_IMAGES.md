# Student Face Images Setup Guide

## How to Add Student Face Images

To make the face recognition system work properly, you need to add student face images in the correct directory structure.

### Directory Structure
Create folders for each student using their registration number as the folder name:

```
resources/labels/
├── REG001/          (Student registration number)
│   ├── 1.png
│   ├── 2.png
│   ├── 3.png
│   ├── 4.png
│   └── 5.png
├── REG002/
│   ├── 1.png
│   ├── 2.png
│   ├── 3.png
│   ├── 4.png
│   └── 5.png
└── ...
```

### Steps to Add Student Images:

1. **Login as Administrator** (admin@gmail.com / @admin_)
2. **Add Students** through the admin panel
3. **Capture 5 clear face images** for each student
4. **Save images** in the format: `resources/labels/{registrationNumber}/{1-5}.png`

### Image Requirements:
- **Format**: PNG files
- **Quality**: Clear, well-lit face images
- **Quantity**: Exactly 5 images per student
- **Naming**: Must be numbered 1.png, 2.png, 3.png, 4.png, 5.png
- **Content**: Only the student's face should be visible

### Troubleshooting:
- If a student is not being recognized, check:
  1. Are the images in the correct folder structure?
  2. Are the images clear and well-lit?
  3. Does the registration number match exactly?
  4. Are there exactly 5 images per student?

### Current Issue:
The system is not marking students as present because:
1. The `resources/labels/` directory was missing
2. No student face images have been added yet
3. The face recognition system cannot find any reference images to match against

**Solution**: Add student face images following the structure above, and the attendance system will start working.
