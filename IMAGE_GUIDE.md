# 📸 How to Add Images to Your Nexus Store

## Folder Structure (Created ✅)
```
Shop/
├── static/
│   └── images/
│       ├── hero.jpg           ← Hero section background
│       ├── men.jpg            ← Men's category card
│       ├── women.jpg          ← Women's category card
│       ├── unisex.jpg         ← Unisex category card
│       └── category-bg.jpg    ← CTA section background
```

## Where to Download Free Images

### Best Free Image Resources:
1. **Unsplash** (unsplash.com) - High quality, free, no credit required
2. **Pexels** (pexels.com) - Free stock photos
3. **Pixabay** (pixabay.com) - Free images & videos
4. **Freepik** (freepik.com) - Free with some restrictions

---

## What Images to Use

### 1. **hero.jpg** (Hero Section Background)
- **Size:** 1920x600px (landscape)
- **Style:** Premium shoes on dark background OR lifestyle shot
- **Search terms:** 
  - "premium shoes dark background"
  - "running shoes lifestyle"
  - "luxury sneakers"
- **Note:** Will have dark overlay (60% opacity) so darker image is better

### 2. **men.jpg** (Men's Category Card)
- **Size:** 400x250px (or larger, will be cropped)
- **Style:** Men's formal shoes + sneakers mix
- **Search terms:**
  - "mens shoes formal casual"
  - "mens footwear collection"
  - "formal sneakers lifestyle"

### 3. **women.jpg** (Women's Category Card)
- **Size:** 400x250px
- **Style:** Women's shoes (heels, sneakers, flats)
- **Search terms:**
  - "womens shoes lifestyle"
  - "womens casual formal shoes"
  - "female footwear collection"

### 4. **unisex.jpg** (Unisex Category Card)
- **Size:** 400x250px
- **Style:** Neutral sneakers, canvas shoes, minimalist
- **Search terms:**
  - "unisex sneakers neutral"
  - "casual canvas shoes"
  - "minimalist footwear"

### 5. **category-bg.jpg** (CTA Section Background)
- **Size:** 1920x400px (landscape)
- **Style:** Shoe close-up, texture, or leather detail
- **Search terms:**
  - "shoe leather texture"
  - "running shoes detail"
  - "shoe fabric macro"
  - "premium shoe material"
- **Note:** Will have dark overlay (70% opacity)

---

## How to Add Images

### Step 1: Download Images
1. Go to Unsplash.com (or any of the above)
2. Search for the term (e.g., "premium shoes dark background")
3. Click the image you like
4. Click "Download" button (usually free)

### Step 2: Save to Correct Folder
- Save each image to: `c:\Users\haris\Desktop\Django\Shop\static\images\`
- Make sure filename matches exactly:
  - `hero.jpg`
  - `men.jpg`
  - `women.jpg`
  - `unisex.jpg`
  - `category-bg.jpg`

### Step 3: Refresh Website
- Go to http://localhost:8000
- Press Ctrl+F5 (hard refresh) to clear cache
- Images should appear!

---

## Quick Unsplash Search Results I Recommend

### Hero.jpg
Search: "premium shoes dark background"
Or: "luxury sneakers lifestyle photography"

### Men.jpg
Search: "mens formal sneakers collection"
Or: "male footwear lifestyle"

### Women.jpg
Search: "womens shoes heels sneakers"
Or: "female footwear collection lifestyle"

### Unisex.jpg
Search: "unisex white sneakers"
Or: "casual canvas shoes flat lay"

### Category-bg.jpg
Search: "leather shoe texture macro"
Or: "running shoe fabric detail"

---

## Image Format Tips

✅ **Do:**
- Use JPG format (compressed, fast)
- Compress images (max 500KB per image)
- Use high resolution (1920x1080+ for hero)
- Make images relevant to shoes

❌ **Don't:**
- Use very large files (slow loading)
- Use watermarked images (unless free to use)
- Use blurry or low quality images
- Mix styles (keep consistent aesthetic)

---

## Image Compression Tool
If images are too large, compress them:
1. Go to: **tinypng.com** or **compressor.io**
2. Upload image
3. Download compressed version
4. Save to folder

---

## After Images Are Added

The website will automatically display:
- ✅ Hero section with image background
- ✅ Category cards with product images
- ✅ CTA section with background image
- ✅ Featured products with images (already working!)

**No code changes needed - just add the image files!**

