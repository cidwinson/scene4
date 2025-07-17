# 📋 ScriptBreakdown Integration Plan

## Current State Analysis

### Data Structure Mismatch:
- **Mock Data**: Uses `Scene` interface with `number`, `heading`, `characters[]`, `props[]`, etc.
- **API Data**: Uses `script_data.scenes[]` with `scene_number`, `scene_header`, `characters_present[]`, `props_mentioned[]`, etc.
- **Current Implementation**: Has dual data sources with complex fallback logic

### Integration Points Identified:

1. **Main Data Flow**: `ScriptBreakdown.vue` → `loadAnalysisData()` → API/Demo data → Display
2. **Scene Selection**: Currently works with mock data structure
3. **Element Filtering**: Processes scene data to extract characters/props/locations
4. **Export Functionality**: Needs to work with both data sources

## 🎯 Integration Plan

### Phase 1: Data Standardization ⭐ **Priority: HIGH**

1. **Create Unified Scene Interface**
   ```typescript
   interface UnifiedScene {
     number: number
     heading: string  
     location: string
     time: string
     characters: string[]
     props: string[]
     notes: string
     budget?: string
     dialogues?: Array<{character: string, text: string}>
   }
   ```

2. **Add Data Transformation Functions**
   ```typescript
   - transformAPIScene(apiScene) → UnifiedScene
   - transformDemoScene(demoScene) → UnifiedScene  
   - standardizeSceneData(scenes[]) → UnifiedScene[]
   ```

### Phase 2: API Integration Enhancement ⭐ **Priority: HIGH**

3. **Enhance loadAnalysisData() Function**
   - Add proper error handling for API scripts
   - Implement consistent data transformation
   - Add loading states for better UX

4. **Update Scene Selection Logic**
   - Make scene selection work with both API and demo data
   - Update `scenes` computed property for consistency
   - Fix scene navigation and jumping

5. **Enhance Project Switching**
   - Detect API scripts vs demo projects
   - Call appropriate data loading methods
   - Handle analysis status checking

### Phase 3: Component Updates ⭐ **Priority: MEDIUM**

6. **Update ScriptPanel.vue**
   - Fix statistics calculation for API data
   - Update scene filtering logic
   - Ensure export works with unified data

7. **Update ElementsPanel.vue**
   - Update element extraction logic
   - Ensure filtering works with unified structure
   - Update element display formatting

### Phase 4: Enhanced Features ⭐ **Priority: LOW**

8. **Add Real-time Analysis Status**
   - Show analysis progress for API scripts
   - Handle incomplete analysis states
   - Add refresh capabilities

9. **Improve Error Handling**
   - Add error boundaries for API failures
   - Show fallback states for missing data
   - Add retry mechanisms

## 🔧 Key Integration Points

### Files to Modify:

1. **`ScriptBreakdown.vue`** - Main integration point
   - Update `loadAnalysisData()` function
   - Standardize `scenes` computed property
   - Add data transformation logic

2. **`stores/projectStore.ts`** - Add helper functions
   - Add `getScriptAnalysisData(scriptId)` function
   - Add data transformation utilities
   - Add analysis status checking

3. **`types/project.ts`** - Standardize interfaces
   - Add `UnifiedScene` interface
   - Update existing interfaces
   - Add API response types

4. **`components/ScriptPanel.vue`** - Update statistics
   - Fix scene count calculation
   - Update character/location statistics
   - Ensure export works with API data

5. **`components/ElementsPanel.vue`** - Update element processing
   - Standardize element extraction
   - Update filtering logic
   - Handle missing data gracefully

## 🎨 User Experience Improvements

### Visual Indicators:
- Show "API Script" vs "Demo Project" badges
- Add analysis status indicators (Complete/Processing/Error)
- Show loading states during data transformation

### Fallback Behavior:
- Graceful degradation when API data is incomplete
- Clear error messages for failed analysis
- Option to retry analysis for failed scripts

## 📊 Data Mapping Strategy

### API → Mock Data Mapping:
```
API Field                   → Mock Field
─────────────────────────── → ─────────────────
scene_number               → number
scene_header               → heading  
characters_present[]       → characters[]
props_mentioned[]          → props[]
location                   → location
time_of_day                → time
action_lines.join()        → notes
estimated_budget           → budget
dialogue_lines[]           → dialogues[]
```

## 🚀 Implementation Priority

1. **IMMEDIATE** (Phase 1): Data standardization and transformation functions
2. **NEXT** (Phase 2): Enhanced API integration in main breakdown view
3. **THEN** (Phase 3): Component updates for consistency
4. **LATER** (Phase 4): Enhanced features and real-time updates

## ✅ Success Criteria

- ✅ API scripts display scenes correctly in breakdown view
- ✅ Scene selection and navigation works for both data sources  
- ✅ Element filtering shows correct characters/props/locations
- ✅ Export functionality works with API data
- ✅ Consistent user experience between API and demo projects
- ✅ Proper error handling and loading states

## Implementation Status

- [x] Phase 1: Data Standardization
  - [x] Created UnifiedScene interface
  - [x] Added data transformation functions (transformAPIScene, transformDemoScene, standardizeSceneData)
  - [x] Added getScriptAnalysisData function
- [x] Phase 2: API Integration Enhancement  
  - [x] Enhanced loadAnalysisData() function with API script support
  - [x] Updated scene selection logic for both API and demo data
  - [x] Added project type detection (api-script vs regular project)
  - [x] Integrated combined projects and scripts loading
- [x] Phase 3: Component Updates
  - [x] Updated ScriptPanel.vue with API data compatibility
  - [x] Added API Script badge indicator
  - [x] Updated ElementsPanel.vue for unified data structure
  - [x] Fixed statistics calculation for both data sources
- [ ] Phase 4: Enhanced Features (Future Enhancement)
  - [ ] Add real-time analysis status
  - [ ] Improve error handling
  - [ ] Add retry mechanisms

## ✅ Integration Complete!

The ScriptBreakdown page now successfully integrates with both API scripts and demo projects:

### **Key Features Implemented:**
- ✅ **Unified Data Structure**: All scenes use standardized format regardless of source
- ✅ **API Script Support**: Loads and displays scenes from analyzed scripts
- ✅ **Project Type Detection**: Automatically detects and handles API scripts vs demo projects
- ✅ **Visual Indicators**: Shows "API Script" badge for scripts from backend analysis
- ✅ **Consistent Statistics**: Character and location counts work for both data sources
- ✅ **Scene Navigation**: Jump to scene and scene selection works across all project types

### **Data Flow:**
```
API Scripts → getScriptAnalysisData() → standardizeSceneData() → Display
Demo Projects → standardizeSceneData() → Display
```

### **User Experience:**
- Users can seamlessly switch between demo projects and analyzed scripts
- All breakdown features (characters, props, locations) work consistently
- Export functionality supports both data sources
- Scene search and filtering work across all project types