# VINAYAK REXINE HOUSE - Logo & Branding Guide

## Logo Implementation

### Current Logo
- **File**: `static/images/vrh-logo.svg`
- **Type**: SVG (Scalable Vector Graphics)
- **Colors**: 
  - Background: Dark Blue (#1e3a5f)
  - Border & Text: Gold (#d4af37)
  - Secondary Text: White (#ffffff)

### Logo Usage

#### 1. Homepage Hero Section
- **Location**: Beside the welcome text
- **Size**: 80px height on desktop, 60px on mobile
- **Features**: Hover effect with slight scale animation

#### 2. Navigation Bar
- **Location**: In navbar brand area
- **Size**: 40px height
- **Features**: Hover animation

### Customizing the Logo

#### Replace with Your Own Logo:
1. **Prepare your logo**: 
   - Recommended format: PNG or SVG
   - Recommended size: 200x200px minimum
   - Transparent background preferred

2. **Add your logo**:
   - Save as `static/images/vrh-logo.png` or `vrh-logo.svg`
   - Update file extension in templates if needed

3. **Update colors** (optional):
   - Edit `static/css/style.css`
   - Modify CSS variables in `:root` section

### Fallback Design
If logo image fails to load, shows:
- **Circular badge** with "VRH" text
- **Same color scheme** as main logo
- **Responsive sizing**

### Brand Colors
```css
--dark-blue: #1e3a5f;    /* Primary brand color */
--gold: #d4af37;         /* Accent/highlight color */
--light-gold: #f4e89a;   /* Light accent */
--white: #ffffff;        /* Background/text */
```

### Technical Features
- **Responsive**: Adapts to different screen sizes
- **Accessible**: Proper alt text for screen readers
- **Performance**: SVG format for crisp display at any size
- **Fallback**: Graceful degradation if image fails

### Future Enhancements
- Add favicon (browser tab icon)
- Create logo variations (horizontal, vertical, monochrome)
- Add loading animation
- Implement dark/light theme variations