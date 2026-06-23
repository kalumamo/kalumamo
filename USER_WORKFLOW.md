# AHADU PULSE - User Workflow Guide
## Updated Workflows After Implementation

---

## For ML Engineers

### New Workflow: Data Upload & Automatic Model Retraining

**Step 1: Login**
- Login to AHADU PULSE with ML Engineer credentials
- Username: ml_engineer@bank.com (or equivalent)
- The dashboard loads and shows all standard pages

**Step 2: Navigate to Model Management**
- Only ML Engineers see "Model Management" in the sidebar navigation
- Click on "Model Management" page
- Other users (Admin, Data Engineers) cannot access this page

**Step 3: Upload Data File**
- On Model Management page, find the upload section
- Click upload area or browse to select CSV/Excel file
- Supported formats: `.csv`, `.xlsx`, `.xls`
- File should contain:
  - `product_code` column (required)
  - `period_date` column (required)
  - Any number of metrics columns

**Step 4: System Automatically Processes**
The system now does this automatically:

**BEFORE (Manual Process):**
- Upload data
- Click "Run Feature Engineering" button
- Wait for completion
- Manually check which products were scored
- Manually retrain models

**AFTER (Automatic Process):**
- Upload data
- System identifies newly uploaded products
- Feature engineering runs automatically for those products only
- Scores recalculated ONLY for new products
- Existing products' scores remain unchanged
- Background model retraining started
- Toast notification shows: "Data processed and rescored for X product(s)"

**Example Workflow:**
```
Upload CSV with 3 products:
  - Product A (new upload)
  - Product B (new upload)
  - Product C (new upload)

System automatically:
  1. Imports all 3 products to database
  2. Computes features for only these 3 products
  3. Calculates scores for only these 3 products
  4. Generates recommendations and alerts for these 3 products
  5. Computes similarity for only these 3 products
  6. Triggers model retraining in background
  7. Shows: "Data processed and rescored for 3 product(s)"

Result:
  - Products A, B, C have new scores
  - All other products' scores remain at previous values
  - No performance impact on existing data
```

**Step 5: View Model Registry**
- After upload processes, scroll to "Model Registry" section
- View all trained models with their metrics
- Click "Auto-Select Best Model" to promote best performing models
- Green highlight shows which model is currently active

**Step 6: Check Drift Detection**
- If model drift is detected, a notification appears
- Shows which models need retraining
- Recommendation provided (e.g., "Retrain Recommended")
- Upload new data to trigger automatic retraining

---

## For Other User Roles

### Product Manager / Executive
- **Cannot** access Model Management page
- If they try: Automatically redirected to Dashboard
- Can see: Products, Scores, Rankings, Predictions, Recommendations
- Can see: Reports and Insights (if role has access)
- Cannot: Upload data, retrain models, manage model registry

### Data Engineer
- **Cannot** access Model Management page (role was restricted)
- Can use: `/data/upload` endpoint programmatically
- Can use: `/data/engineer` endpoint programmatically
- Cannot: View `/ml/models` endpoint response
- Recommendation: Use API directly with specific script

### Super Admin
- **Can** access Model Management page (admin override)
- Full access to all ML operations
- Can upload data, view models, retrain
- Should delegate to ML Engineer for daily operations

---

## Single Product Upload Scenario

### Scenario: Update One Product's Data

**File Content:**
```
product_code, period_date, active_users, transactions, revenue
PRD-001,     2026-06-21, 1500,          500,          150000
```

**Workflow:**
1. Upload CSV with 1 row
2. System response: `newly_uploaded_product_ids: [1]`
3. Feature engineering runs for product ID 1 only
4. Only product 1 gets new score
5. All 50+ other products retain their scores

**Toast Message:**
```
✓ Data processed and rescored for 1 product
```

**Result:**
- Product 1: New score calculated
- Products 2-50+: Scores unchanged

---

## Multiple Products Upload Scenario

### Scenario: Monthly Data Batch

**File Content:**
```
product_code, period_date,    active_users, transactions, revenue
PRD-001,      2026-06-21,     1500,         500,          150000
PRD-002,      2026-06-21,     2000,         600,          180000
PRD-003,      2026-06-21,     800,          250,          75000
PRD-005,      2026-06-21,     1200,         400,          120000
```

**Workflow:**
1. Upload CSV with 4 rows (4 unique products)
2. System response: `newly_uploaded_product_ids: [1, 2, 3, 5]`
3. Feature engineering runs for products 1, 2, 3, 5 only
4. Only these 4 products get new scores
5. All other products retain scores from previous periods

**Toast Message:**
```
✓ Data processed and rescored for 4 product(s)
```

**Result:**
- Products 1, 2, 3, 5: New scores calculated
- Products 4, 6-50+: Scores unchanged from previous period

---

## Prediction Page Workflow

### If Models Are Trained

**Workflow:**
1. Click "Predictions & Forecast" in sidebar
2. Page loads all available predictions
3. Shows 3-month forward forecasts for all products
4. Filter by product if needed
5. View trend direction: Improving, Stable, or Declining

### If No Models Trained Yet

**Workflow:**
1. Click "Predictions & Forecast" in sidebar
2. Page shows empty state with message:
   ```
   No predictions available yet
   Train models and upload data to generate predictions
   ```
3. Next steps:
   - Go to Model Management
   - Upload data file
   - System trains models automatically
   - Return to Predictions page (data should appear within seconds)

### Error Scenarios

**If Error Occurs:**
- Toast shows helpful error message
- Page displays empty state (not broken)
- No crash or 500 error page
- User can retry

---

## Model Selection Workflow

### Manual Best Model Selection

1. In Model Management, scroll to "Auto-Select Best Model" section
2. See summary: Current active classifier and regressor
3. Click "Select Best" button
4. System evaluates all trained models
5. Selects best by loss (lowest loss = best)
6. Promotes selected models to ACTIVE status
7. Results show: "Best model selected" toast
8. Model Registry updates to show green BEST badges

### Automatic Selection (Optional)

- Run daily/weekly scheduled job
- Calls `POST /ml/select-best` automatically
- Best models stay current without manual intervention

---

## Troubleshooting

### Problem: Model Management Page Shows "Permission Denied"
**Solution**: You are not logged in as ML Engineer
- Verify your user role in Settings > Profile
- Contact admin to add ml_engineer role to your account

### Problem: Scores Not Updating After Upload
**Solution**: Check upload response
- Was upload status "success"?
- Check rows_imported > 0?
- Products not previously in system show as new
- If reupload known product: Product score updates

### Problem: Predictions Page Shows "No predictions available"
**Solution**: Models not yet trained
- Go to Model Management
- Upload data file (with real data)
- Wait for automatic processing
- Return to Predictions (models now trained)

### Problem: Auto-Select Best Model Failed
**Solution**: Not enough models trained
- You need at least 2 classifier models OR
- You need at least 1 regression model
- Train multiple models first, then retry

---

## Security Notes

### Access Control

**Model Management Page:**
- ✅ Hidden from sidebar for non-engineers
- ✅ Blocked by route redirect if manually accessed
- ✅ Backend API validates role

**Model Registry:**
- ✅ Only accessible to ml_engineer role
- ✅ Data engineers cannot view
- ✅ Read-only for all roles (no delete/edit)

### Data Privacy

**Product Scores:**
- Each upload creates distinct scored set
- Existing product scores never modified
- Full audit trail of who uploaded when
- No data loss on partial uploads

---

## API for Developers

### Upload Data and Auto-Retrain

**Request:**
```bash
curl -X POST http://localhost:5000/api/data/upload \
  -H "Authorization: Bearer {token}" \
  -F "file=@data.csv"
```

**Response:**
```json
{
  "status": "success",
  "filename": "data.csv",
  "rows_imported": 10,
  "rows_failed": 0,
  "batch_id": "uuid-here",
  "newly_uploaded_product_ids": [1, 2, 3, 5],
  "message": "Imported 10 row(s). Click 'Run Feature Engineering' to compute scores..."
}
```

### Selective Scoring

**Request:**
```bash
curl -X POST http://localhost:5000/api/data/engineer \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"product_ids": [1, 2, 3]}'
```

**Response:**
```json
{
  "message": "Feature engineering completed for 10 record(s).",
  "features_computed": 10,
  "products_scored": [
    {
      "product_id": 1,
      "period_date": "2026-06-21",
      "score": 85.50,
      "tier": "HIGH"
    },
    ...
  ]
}
```

---

## Best Practices

1. **Upload Frequency**: Daily or weekly batches recommended
2. **Batch Size**: 10-50 products per upload optimal
3. **Data Quality**: Validate data before upload (missing values OK, invalid product codes cause errors)
4. **Score Review**: Check new scores after upload (spot check 2-3 products)
5. **Model Monitoring**: Review drift detection weekly
6. **Auto-Select**: Run best model selection after every model training batch

---

## Implementation Checklist

- [ ] ML Engineer can upload data
- [ ] Upload returns newly_uploaded_product_ids
- [ ] Feature engineering uses product_ids for selective scoring
- [ ] Only new products' scores updated
- [ ] Existing products' scores unchanged
- [ ] Toast shows correct product count
- [ ] Predictions page shows helpful empty state
- [ ] Predictions page handles errors gracefully
- [ ] Model Management accessible only to ml_engineer
- [ ] Other roles redirected away from Model Management
- [ ] Sidebar doesn't show Model Management to non-engineers
- [ ] /ml/models endpoint restricts to ml_engineer

---

## Summary

**What Changed:**
- ✅ Automatic model retraining (no manual button)
- ✅ Selective product rescoring (new products only)
- ✅ ML Engineer role enforcement (Model Management page)
- ✅ Improved error handling (Predictions page)
- ✅ Better empty states (user guidance)

**What Stayed the Same:**
- All existing API endpoints work as before
- All existing roles/permissions
- All existing data in database
- All existing product scores (when not retraining)

**User Impact:**
- ML Engineers: Faster workflow, automatic processing
- Other Users: No changes, same access as before
- Admins: Can still access if needed, but shouldn't
- System: Reduced unnecessary reprocessing, better performance

