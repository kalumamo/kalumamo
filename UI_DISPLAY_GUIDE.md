# UI Display Guide - Where to See the Changes

**Location**: Model Management Page (`/dashboard/models`)  
**Device**: Web browser

---

## UPLOAD SECTION

### Before Upload
```
┌─────────────────────────────────────────────┐
│ Upload New Data                             │
├─────────────────────────────────────────────┤
│                                             │
│         [📤 Upload Icon]                   │
│    Drop file or click to browse             │
│    CSV, XLSX, or XLS (max 10MB)             │
│                                             │
└─────────────────────────────────────────────┘
```

### After Successful Upload - Product Scores Display
```
┌─────────────────────────────────────────────┐
│ ✅ Upload Successful                        │
├─────────────────────────────────────────────┤
│ Rows imported: 1                            │
│ Rows failed: 0                              │
│                                             │
│ ═════════════════════════════════════════   │
│ 📊 Product Scores                           │
│ ═════════════════════════════════════════   │
│                                             │
│ ┌─────────────────────────────────────┐   │
│ │ Product ID: 5        [HIGH] 🟢     │   │
│ │                                     │   │
│ │ Period: 2026-06-21                 │   │
│ │ Previous: 70.00                    │   │
│ │                   **72.50** ↑       │   │
│ │ ↑ +2.50 points (+3.6%)             │   │
│ │                                     │   │
│ └─────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

### With Multiple Products
```
┌─────────────────────────────────────────────┐
│ ✅ Upload Successful                        │
├─────────────────────────────────────────────┤
│ Rows imported: 3                            │
│ Rows failed: 0                              │
│                                             │
│ ═════════════════════════════════════════   │
│ 📊 Product Scores                           │
│ ═════════════════════════════════════════   │
│                                             │
│ ┌─────────────────────────────────────┐   │
│ │ Product ID: 1        [HIGH] 🟢     │   │
│ │ Period: 2026-06-21                 │   │
│ │ Previous: 65.00                    │   │
│ │                   **78.50** ↑       │   │
│ │ ↑ +13.50 points (+20.8%)           │   │
│ └─────────────────────────────────────┘   │
│                                             │
│ ┌─────────────────────────────────────┐   │
│ │ Product ID: 2        [MEDIUM] 🟡   │   │
│ │ Period: 2026-06-21                 │   │
│ │ Previous: 55.00                    │   │
│ │                   **58.25** ↑       │   │
│ │ ↑ +3.25 points (+5.9%)             │   │
│ └─────────────────────────────────────┘   │
│                                             │
│ ┌─────────────────────────────────────┐   │
│ │ Product ID: 3        [LOW] 🔴       │   │
│ │ Period: 2026-06-21                 │   │
│ │ Previous: 42.00                    │   │
│ │                   **45.75** ↑       │   │
│ │ ↑ +3.75 points (+8.9%)             │   │
│ └─────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

---

## SCORE DISPLAY DETAILS

### Product Card Components

**Header Row**
```
Product ID: 5  [TIER BADGE]

- Product ID: Left-aligned, bold
- Tier Badge: Right side with color
  - HIGH: Green badge (🟢)
  - MEDIUM: Yellow badge (🟡)
  - LOW: Red badge (🔴)
```

**Information Row**
```
Period: 2026-06-21                Previous: 70.00

- Left: Small text with date
- Right: Previous score shown
```

**Score Row (Highlighted)**
```
                            **72.50**
                      Current Score (Large, Bold)
```

**Change Row (Colored)**
```
↑ +2.50 points (+3.6%)

- Arrow: ↑ Green (up), ↓ Red (down), → Gray (same)
- Change: Absolute points change
- Percentage: Relative change percentage
- Color: Green if positive, Red if negative, Gray if no change
```

---

## PREDICTIONS PAGE - CONFIDENCE DISPLAY

### Before (BAD - 100% Confidence)
```
┌─────────────────────────────────────┐
│ Month 1 - 2026-07-21               │
│ Score: 85.0                        │
│ Tier: [HIGH] 🟢                    │
│ Confidence: 100% ❌ (Unrealistic)  │
│ ┌─────────────────────────────┐   │
│ │█████████████████████████│ 100% │
│ └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

### After (GOOD - Realistic Confidence)
```
┌─────────────────────────────────────┐
│ Month 1 - 2026-07-21               │
│ Score: 85.0                        │
│ Tier: [HIGH] 🟢                    │
│ Confidence: 89% ✅ (Realistic)     │
│ ┌─────────────────────────────┐   │
│ │███████████████████████░░░│ 89% │
│ └─────────────────────────────┘   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Month 2 - 2026-08-21               │
│ Score: 86.5                        │
│ Tier: [HIGH] 🟢                    │
│ Confidence: 91% ✅ (Realistic)     │
│ ┌─────────────────────────────┐   │
│ │███████████████████████░░░│ 91% │
│ └─────────────────────────────┘   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ Month 3 - 2026-09-21               │
│ Score: 87.2                        │
│ Tier: [HIGH] 🟢                    │
│ Confidence: 92% ✅ (Max Cap)       │
│ ┌─────────────────────────────┐   │
│ │███████████████████████░░│ 92%  │
│ └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

### Confidence Range
```
Minimum: 75% (baseline, when no classifier available)
Maximum: 92% (capped to avoid unrealistic 100%)

Example values:
- Rule-based only: 75%
- With weak classifier: 80-85%
- With good classifier: 85-92%
- Never: 100% ❌
```

---

## TOAST NOTIFICATIONS

### After Upload Starts
```
Processing data...  ⟳
```

### After Upload Completes
```
✅ Data processed and rescored for 1 product
```

### If Error
```
❌ Upload failed: Invalid file format
```

---

## PAGE STRUCTURE

### Full Model Management Layout
```
┌─────────────────────────────────────────────────┐
│ HEADER: Model Management                        │
│ Subtitle: Upload data to automatically retrain  │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ UPLOAD SECTION (Step 1)                         │
│ ┌─────────────────────────────────────────────┐ │
│ │ Upload area + Result with Scores Display    │ │  ← YOU ARE HERE
│ └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ AUTO-SELECT BEST MODEL (Step 2)                 │
│ ┌─────────────────────────────────────────────┐ │
│ │ [Select Best] button for model selection    │ │
│ └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ DRIFT DETECTION (Step 3)                        │
│ ┌─────────────────────────────────────────────┐ │
│ │ Model drift monitoring status               │ │
│ └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ MODEL REGISTRY (Step 4)                         │
│ ┌─────────────────────────────────────────────┐ │
│ │ Table of all trained models                 │ │
│ └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

---

## USER INTERACTION FLOW

### Scenario 1: Upload Single Product
```
1. Click upload area
   ↓
2. Select file (1 row, 1 product)
   ↓
3. System processes (~2 seconds)
   ↓
4. ✅ GREEN CARD APPEARS with:
   - Upload Successful message
   - 1 row imported, 0 failed
   - 📊 PRODUCT SCORES section
   - Product ID: 5
   - Period: 2026-06-21
   - **72.50** (big bold number)
   - ↑ +2.50 points (+3.6%)
   ↓
5. Toast: "Data processed and rescored for 1 product"
   ↓
6. DONE - No need to do anything else!
```

### Scenario 2: Upload Multiple Products
```
1. Click upload area
   ↓
2. Select file (3 rows, 3 products)
   ↓
3. System processes (~5 seconds)
   ↓
4. ✅ GREEN CARD APPEARS with:
   - Upload Successful message
   - 3 rows imported, 0 failed
   - 📊 PRODUCT SCORES section shows:
     ✓ Product 1 card
     ✓ Product 2 card
     ✓ Product 3 card
   - Each with score, change, percentage
   ↓
5. Toast: "Data processed and rescored for 3 products"
   ↓
6. DONE - All scores visible!
```

---

## COLOR CODING

### Tier Colors
- 🟢 HIGH: Green background (bg-green-100)
- 🟡 MEDIUM: Yellow background (bg-yellow-100)
- 🔴 LOW: Red background (bg-red-100)

### Change Indicators
- ↑ Green: Score increased (positive)
- ↓ Red: Score decreased (negative)
- → Gray: Score unchanged (neutral)

### Status Colors
- Green: Upload successful, processing done
- Red: Upload failed, error occurred
- Gray: Neutral information

---

## RESPONSIVE DESIGN

### Desktop (1920px+)
- Full width upload card
- Product cards display side-by-side
- All information visible at once

### Tablet (768px - 1024px)
- Slightly narrower upload card
- Product cards stack
- Information remains readable

### Mobile (< 768px)
- Full-width cards
- Smaller font sizes
- All scores still visible and readable

---

## ACCESSIBILITY

- ✅ Color-blind friendly (uses both color AND text)
- ✅ Screen reader compatible (proper labels)
- ✅ High contrast (accessible text colors)
- ✅ Keyboard navigable (clickable areas)
- ✅ Large touch targets (mobile-friendly)

---

## ANIMATIONS

- Upload area: Hover effect changes border color and background
- Cards appear: Smooth fade-in (if implemented)
- Toast: Appears from bottom, auto-dismisses after 5 seconds
- Progress: Loading states with animation while processing

---

**Summary**: All product score information displays immediately after upload on the same page. No navigation needed!
