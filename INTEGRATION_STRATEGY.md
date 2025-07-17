# Winson Integration Strategy & Action Blueprint

## 🔍 ROOT CAUSE ANALYSIS

### Critical Issues Identified

1. **DUAL STORE ARCHITECTURE CONFLICT**
   - `/frontend/src/stores/projectStore.ts` - Simple local storage only (addProject method)
   - `/frontend/frontend_stores/projectStore.ts` - Full API integration (analyzeAndSave method)
   - **Impact**: NewProject.vue imports the wrong store, bypassing API calls entirely

2. **API ENDPOINT MISMATCH**
   - Backend provides: `/analyze-script` + `/save-analysis` (separate endpoints)
   - Frontend store calls: Combined `analyzeAndSave()` method
   - **Impact**: Works correctly but requires both endpoints to be available

3. **DATABASE CONNECTION NOT INITIALIZED**
   - PostgreSQL configured in `.env` but no server startup process
   - Tables not created automatically
   - **Impact**: API calls fail silently or return database errors

4. **MISSING SERVER STARTUP**
   - No active FastAPI server running on localhost:8000
   - Multiple Python scripts but no clear entry point
   - **Impact**: All API calls result in network connection failures

## 🎯 INTEGRATION STRATEGY

### Phase 1: Immediate Fixes (Critical)

#### 1.1 Fix Store Import in NewProject.vue
**Current Issue**: Wrong projectStore imported
```typescript
// WRONG (current)
import { useProjectStore } from '../stores/projectStore'

// CORRECT (needed)
import { useProjectStore } from '../../frontend_stores/projectStore'
```

#### 1.2 Start Backend Server
**Required Actions**:
1. Install Python dependencies: `pip install -r requirements.txt`
2. Setup PostgreSQL database: Create database "Scenesplit"
3. Start server: `python start_server.py`
4. Verify endpoints: `curl http://localhost:8000/health`

#### 1.3 Database Initialization
**Required Setup**:
```bash
# 1. Ensure PostgreSQL is running
# 2. Create database
createdb -U postgres Scenesplit

# 3. Initialize tables
python -c "from database.database import init_database; init_database()"
```

### Phase 2: Architectural Consolidation

#### 2.1 Store Consolidation Options

**Option A: Merge Stores (Recommended)**
- Move API methods from `frontend_stores/projectStore.ts` to `src/stores/projectStore.ts`
- Maintain single source of truth
- Update all imports to use consolidated store

**Option B: Clear Separation**
- Keep `src/stores/projectStore.ts` for UI state only
- Keep `frontend_stores/projectStore.ts` for API operations only
- Create clear naming convention (e.g., `useUIStore` vs `useAPIStore`)

#### 2.2 Error Handling Enhancement
```typescript
// Add to NewProject.vue
async function onAnalyzeAndSave() {
  try {
    // 1. Check backend health first
    const health = await projectStore.checkHealth()
    if (!health) throw new Error('Backend server not available')
    
    // 2. Proceed with analysis
    const result = await projectStore.analyzeAndSave(selectedFile.value)
    
    // 3. Handle success/failure
    if (result?.success) {
      router.push({ name: 'ProjectsView' })
    } else {
      throw new Error(projectStore.error || 'Analysis failed')
    }
  } catch (error) {
    // Clear error display with fallback options
    showError(error.message)
  }
}
```

### Phase 3: Production Readiness

#### 3.1 Environment Configuration
```env
# Frontend (.env)
VITE_API_BASE_URL=http://localhost:8000

# Backend (.env)
DB_USER=postgres
DB_PASSWORD=winsonlim
DB_HOST=localhost
DB_PORT=5432
DB_NAME=Scenesplit
```

#### 3.2 Docker Containerization
```dockerfile
# Backend Dockerfile
FROM python:3.9
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "start_server.py"]

# Frontend Dockerfile
FROM node:18
COPY package*.json .
RUN npm install
COPY . .
CMD ["npm", "run", "dev"]
```

## 🚀 ACTION BLUEPRINT

### Immediate Actions (Next 30 minutes)

#### Step 1: Fix Critical Import
```bash
# File: /frontend/src/views/NewProject.vue
# Line 112: Change import path
```

#### Step 2: Start Backend Infrastructure
```bash
cd backend_zarul
pip install -r requirements.txt
python start_server.py
```

#### Step 3: Test Integration
```bash
# 1. Open frontend in browser
# 2. Upload a PDF file
# 3. Click Generate button
# 4. Check browser dev tools for API calls
# 5. Verify database entries in pgAdmin
```

### Validation Checklist

- [ ] Backend server responds at `http://localhost:8000/health`
- [ ] Database "Scenesplit" exists and is accessible
- [ ] Frontend imports correct projectStore
- [ ] Generate button triggers `analyzeAndSave()` method
- [ ] API calls visible in browser Network tab
- [ ] Database entries created in AnalyzedScript table
- [ ] Success navigation to ProjectsView
- [ ] Error handling displays meaningful messages

### Troubleshooting Guide

#### Issue: "Network Error" when clicking Generate
**Solution**: Backend server not running
```bash
cd backend_zarul && python start_server.py
```

#### Issue: "Database connection failed"
**Solution**: PostgreSQL not running or database doesn't exist
```bash
# Start PostgreSQL service
sudo service postgresql start

# Create database
createdb -U postgres Scenesplit
```

#### Issue: "Analysis failed" with no errors
**Solution**: Check backend logs and API response
```bash
# Check server logs
# Check browser dev tools Network tab
# Verify file upload format
```

#### Issue: Generate button doesn't respond
**Solution**: Check if correct store is imported
```typescript
// Verify import in NewProject.vue
console.log(projectStore.analyzeAndSave) // Should be function
```

## 📁 PROJECT STRUCTURE OVERVIEW

```
winson/
├── backend_zarul/           # FastAPI backend
│   ├── api/api.py          # Main API endpoints
│   ├── database/           # PostgreSQL integration
│   ├── start_server.py     # Server startup script
│   └── .env               # Database credentials
├── frontend/
│   ├── src/stores/         # Local UI state store
│   ├── frontend_stores/    # API integration store ⭐
│   └── src/views/NewProject.vue # File upload component
└── INTEGRATION_STRATEGY.md # This file
```

## 🔧 DEBUGGING TOOLS

### Frontend Debug Commands
```javascript
// Browser console debugging
console.log(projectStore.analyzeAndSave) // Check if method exists
console.log(projectStore.API_BASE)       // Check API URL
```

### Backend Debug Commands
```bash
# Test API endpoints directly
curl -X GET http://localhost:8000/health
curl -X POST http://localhost:8000/analyze-script -F "file=@test.pdf"
```

### Database Debug Commands
```sql
-- Check if tables exist
\dt

-- Check recent entries
SELECT * FROM analyzed_scripts ORDER BY created_at DESC LIMIT 5;
```

## 🎯 SUCCESS METRICS

1. **Functional Integration**: Generate button successfully processes files
2. **Database Persistence**: Scripts saved and retrievable from PostgreSQL
3. **Error Resilience**: Meaningful error messages for common failure modes
4. **Performance**: Analysis completes within 30 seconds for typical scripts
5. **UI Feedback**: Progress indicators and status updates work correctly

---

**Next Action**: Execute Step 1-3 of the Action Blueprint to resolve immediate integration issues.