<template>
  <div class="transition-all duration-300" :class="sidebarExpanded ? 'ml-64' : 'ml-16'">
    <!-- Header Section -->
    <div
      class="w-full relative bg-background-primary h-20 flex flex-row items-center justify-between py-[15px] pl-[19px] pr-[104px] box-border gap-0 text-left text-2xl text-white font-inter z-30 border-b border-gray-700"
      style="position: sticky; top: 0;"
    >
      <div class="flex items-center gap-6">
        <h1 class="relative leading-[28.8px] font-inter-bold">Budget Management</h1>
        <div class="flex items-center gap-4">
          <select
            v-model="selectedProjectLocal"
            class="bg-background-tertiary text-secondary font-inter-semibold rounded-lg px-4 py-2 focus:outline-none border border-gray-600 focus:border-secondary transition-colors"
          >
            <option
              v-for="project in projects"
              :key="project.title"
              :value="project.title"
              class="bg-background-tertiary text-white"
            >
              {{ project.title }}
            </option>
          </select>
          
          <!-- Confirm Button -->
          <button
            @click="confirmProjectChange"
            :disabled="selectedProjectLocal === selectedProjectTitle || budgetLoading"
            :class="[
              'px-4 py-2 rounded-lg font-inter-semibold text-sm transition-colors',
              selectedProjectLocal === selectedProjectTitle || budgetLoading
                ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                : 'bg-secondary text-black hover:bg-secondary-hover cursor-pointer'
            ]"
          >
            <span v-if="budgetLoading">Loading...</span>
            <span v-else>Confirm</span>
          </button>
          
          <!-- Budget Source Indicator -->
          <div v-if="selectedProject" class="flex items-center gap-2">
            <span
              v-if="selectedProject.type === 'api-script'"
              class="text-xs font-inter-bold px-3 py-1 rounded whitespace-nowrap bg-blue-500 text-white"
            >
              API Budget
            </span>
            <span
              v-else
              class="text-xs font-inter-bold px-3 py-1 rounded whitespace-nowrap bg-green-500 text-white"
            >
              Demo Budget
            </span>
          </div>
        </div>
      </div>
      <div class="flex flex-row items-center justify-start gap-4 text-sm text-text-secondary">
        <div class="w-[100px] rounded-lg bg-gray-700 h-10 flex flex-row items-center justify-center gap-2 text-text-secondary cursor-pointer hover:bg-gray-600 transition-colors">
          <img class="w-4 h-4" alt="" src="../assets/icon/download.svg" />
          <div class="leading-[16.8px] font-inter-medium">Export</div>
        </div>
        <div class="w-[120px] rounded-lg bg-secondary h-10 flex flex-row items-center justify-center gap-1 cursor-pointer text-black hover:bg-secondary-hover transition-colors" @click="showAI = true">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
          </svg>
          <div class="leading-[16.8px] font-inter-semibold">AI Assistant</div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="bg-background-primary h-[calc(100vh-80px)] overflow-y-auto">
      <div class="p-6">
        <div class="max-w-7xl mx-auto flex flex-col gap-6">

          <!-- Budget Breakdown -->
          <div class="bg-background-secondary rounded-2xl p-8 border border-gray-700">
            <div class="flex items-center justify-between mb-6">
              <div class="text-lg font-inter-bold text-white">Budget Breakdown by Category</div>
              <div class="flex items-center gap-2">
                <button class="bg-background-tertiary rounded-lg px-3 py-2 text-text-muted hover:text-white transition-colors flex items-center gap-1 border border-gray-600">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path d="M4 6h16M4 12h16M4 18h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                </button>
                <button class="bg-background-tertiary rounded-lg px-3 py-2 text-text-muted hover:text-white transition-colors flex items-center gap-1 border border-gray-600">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                    <path d="M12 8v4l2 2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  </svg>
                </button>
              </div>
            </div>
            <!-- Loading State -->
            <div v-if="budgetLoading" class="flex items-center justify-center py-12">
              <div class="flex items-center gap-3">
                <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-secondary"></div>
                <span class="text-text-muted font-inter-medium">Loading budget data...</span>
              </div>
            </div>
            
            <!-- Error State -->
            <div v-else-if="budgetError" class="flex items-center justify-center py-12">
              <div class="text-center">
                <div class="text-red-400 font-inter-medium mb-2">Failed to load budget data</div>
                <div class="text-text-muted text-sm">{{ budgetError }}</div>
                <button 
                  @click="loadBudgetData" 
                  class="mt-4 bg-secondary hover:bg-secondary-hover text-black px-4 py-2 rounded-lg font-inter-semibold text-sm transition-colors"
                >
                  Retry
                </button>
              </div>
            </div>
            
            <!-- Budget Breakdown Data -->
            <div v-else-if="breakdown.length" class="space-y-5">
              <template v-for="cat in breakdown" :key="cat.name">
                <div class="mb-5">
                  <div class="flex items-center justify-between mb-2">
                    <div class="font-inter-semibold text-white" :style="{ color: cat.color }">{{ cat.name }}</div>
                    <div class="flex items-center gap-3">
                      <div class="font-inter-semibold text-white" :style="{ color: cat.color }">{{ cat.amount }}</div>
                      <button 
                        @click="editBudgetCategory(cat)"
                        class="bg-background-tertiary hover:bg-gray-600 rounded-lg p-2 transition-colors border border-gray-600 text-text-muted hover:text-white"
                        title="Edit budget amount"
                      >
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                        </svg>
                      </button>
                    </div>
                  </div>
                  <div class="flex items-center gap-4">
                    <div class="flex-1 h-3 rounded-lg bg-background-tertiary relative overflow-hidden">
                      <div
                        class="h-3 rounded-lg absolute left-0 top-0 transition-all duration-300"
                        :style="{ width: cat.percent + '%', background: cat.color }"
                      ></div>
                    </div>
                    <div class="text-text-muted text-xs w-14 font-inter-regular">{{ cat.percent }}%</div>
                  </div>
                </div>
              </template>
            </div>
            <div v-else class="text-center py-12">
              <div class="text-text-muted font-inter-regular mb-4">No budget data available for this project.</div>
              <div class="text-text-muted text-sm font-inter-regular">Budget breakdown will appear here once the project has budget information.</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- AI Assistant Panel -->
    <Transition
      enter-active-class="transition-transform duration-300 ease-out"
      enter-from-class="transform translate-x-full"
      enter-to-class="transform translate-x-0"
      leave-active-class="transition-transform duration-300 ease-in"
      leave-from-class="transform translate-x-0"
      leave-to-class="transform translate-x-full"
    >
      <AIChatPanel v-if="showAI" class="fixed top-0 right-0 z-50" @close="showAI = false" />
    </Transition>

    <!-- Budget Edit Modal -->
    <div v-if="editingCategory" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-background-secondary rounded-xl p-6 w-full max-w-md border border-gray-700">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-inter-bold text-white">Edit Budget Category</h3>
          <button @click="cancelBudgetEdit" class="text-text-muted hover:text-white">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>
        
        <div class="space-y-4">
          <div>
            <label class="block text-text-secondary text-sm font-inter-medium mb-2">Category</label>
            <div class="text-white font-inter-semibold" :style="{ color: editingCategory.color }">
              {{ editingCategory.name }}
            </div>
          </div>
          
          <div>
            <label class="block text-text-secondary text-sm font-inter-medium mb-2">Amount (RM)</label>
            <input
              v-model="editAmount"
              type="number"
              min="0"
              step="0.01"
              class="w-full px-4 py-3 rounded-lg bg-background-tertiary text-white border border-gray-600 focus:outline-none focus:border-secondary focus:ring-2 focus:ring-secondary/20 transition-all font-inter-regular"
              placeholder="Enter amount"
            />
          </div>
        </div>
        
        <div class="flex gap-3 mt-6">
          <button
            @click="cancelBudgetEdit"
            class="flex-1 py-3 px-4 rounded-lg bg-background-tertiary text-text-secondary hover:text-white transition-colors border border-gray-600 font-inter-medium"
          >
            Cancel
          </button>
          <button
            @click="saveBudgetEdit"
            class="flex-1 py-3 px-4 rounded-lg bg-secondary text-black hover:bg-secondary-hover transition-colors font-inter-semibold"
          >
            Save Changes
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, inject, watch, onMounted } from 'vue'
import AIChatPanel from '../components/AIChatPanel.vue'
import { useProjectStore } from '../stores/projectStore'

const sidebarExpanded = inject('sidebarExpanded', ref(false))

const showAI = ref(false)
const projectStore = useProjectStore()
// Combine regular projects and API scripts
const projects = computed(() => {
  const regularProjects = projectStore.projects
  const apiScripts = projectStore.scripts.map(script => ({
    id: `api-${script.id}`,
    script_id: script.id,
    title: script.title || script.filename,
    description: script.description || `Analyzed script: ${script.filename}`,
    status: script.status === 'completed' ? 'COMPLETED' : 'ACTIVE',
    created_at: script.created_at,
    script_filename: script.filename,
    type: 'api-script',
    budget_total: script.estimated_budget || 0,
    estimated_duration_days: script.estimated_duration_days || 0,
    scripts_count: script.total_scenes || 0
  }))
  
  return [...regularProjects, ...apiScripts]
})

const selectedProjectTitle = ref(projectStore.selectedProjectTitle || projects.value[0]?.title || '')
const selectedProjectLocal = ref(selectedProjectTitle.value)

// Find the selected project object
const selectedProject = computed(() =>
  projects.value.find(p => p.title === selectedProjectTitle.value)
)

// Budget data state
const budgetData = ref<any>(null)
const budgetLoading = ref(false)
const budgetError = ref<string | null>(null)

// Watch for prop changes to sync local state
watch(() => projectStore.selectedProjectTitle, (newTitle) => {
  selectedProjectTitle.value = newTitle
  selectedProjectLocal.value = newTitle
})

// Handle project change
function onProjectChange() {
  projectStore.setSelectedProject(selectedProjectTitle.value)
}

// Load budget data for current project
async function loadBudgetData() {
  const project = selectedProject.value
  if (!project) return

  budgetLoading.value = true
  budgetError.value = null

  try {
    console.log('Loading budget data for project:', project.title, 'Type:', project.type, 'ID:', project.id)
    
    // For API scripts, ensure the store has the project in its projects list
    if (project.type === 'api-script') {
      // Add this project to the store's projects if not already there
      const storeProject = projectStore.projects.find(p => p.id === project.id)
      if (!storeProject) {
        projectStore.projects.push(project)
        console.log('Added API script project to store')
      }
    }
    
    budgetData.value = await projectStore.getBudgetBreakdown(project.id)
    console.log('Loaded budget data:', budgetData.value)
  } catch (error: any) {
    console.error('Failed to load budget data:', error)
    budgetError.value = error.message || 'Failed to load budget data'
  } finally {
    budgetLoading.value = false
  }
}

// Confirm project change
async function confirmProjectChange() {
  if (selectedProjectLocal.value !== selectedProjectTitle.value) {
    console.log('Confirming budget project change to:', selectedProjectLocal.value)
    selectedProjectTitle.value = selectedProjectLocal.value
    projectStore.setSelectedProject(selectedProjectLocal.value)
    
    // Load budget data for new project
    await loadBudgetData()
  }
}

// Helper: parse RM value to number
function parseRM(val: string | number | unknown): number {
  if (!val) return 0
  const stringVal = String(val)
  return Number(stringVal.replace(/[^\d.]/g, ''))
}

// Budget editing
const editingCategory = ref<any>(null)
const editAmount = ref('')

function editBudgetCategory(category: any) {
  editingCategory.value = category
  editAmount.value = parseRM(category.amount).toString()
}

async function saveBudgetEdit() {
  if (!editingCategory.value || !selectedProject.value) return
  
  try {
    const newAmount = Number(editAmount.value)
    if (isNaN(newAmount) || newAmount < 0) {
      alert('Please enter a valid amount')
      return
    }
    
    const project = selectedProject.value
    const categoryKey = editingCategory.value.key
    
    // Use the store's updateBudgetCategory function
    const success = await projectStore.updateBudgetCategory(project.id, categoryKey, newAmount)
    
    if (success) {
      // Update local budget data
      if (budgetData.value) {
        budgetData.value[categoryKey] = newAmount
        // Recalculate total
        const categories = ['talent', 'location', 'propsSet', 'wardrobeMakeup', 'sfxVfx', 'crew', 'miscellaneous']
        budgetData.value.total = categories.reduce((sum, key) => sum + (budgetData.value[key] || 0), 0)
      }
      
      console.log('Budget updated successfully')
    } else {
      if (project.type === 'api-script') {
        alert('Budget editing for API scripts is not yet implemented')
      } else {
        alert('Failed to update budget')
      }
    }
    
    editingCategory.value = null
    editAmount.value = ''
  } catch (error) {
    console.error('Failed to save budget edit:', error)
    alert('Failed to save changes. Please try again.')
  }
}

function cancelBudgetEdit() {
  editingCategory.value = null
  editAmount.value = ''
}

// Remove the summary computed property since we're not using budget summary cards anymore

// Budget breakdown by category with improved colors
const categoryColors: Record<string, string> = {
  talent: '#00C6FB',
  location: '#FFD233', 
  propsSet: '#3DD65B',
  wardrobeMakeup: '#A259FF',
  sfxVfx: '#FF6B6B',
  crew: '#FF9900',
  miscellaneous: '#FFB300'
}

const breakdown = computed(() => {
  if (!budgetData.value || budgetData.value.total === 0) {
    return []
  }

  const total = budgetData.value.total
  // Only show the 5 requested categories: Talent, Location, Crew, Props & Set, Wardrobe & Makeup
  const categories = ['talent', 'location', 'crew', 'propsSet', 'wardrobeMakeup']
  
  return categories
    .map(key => {
      const amount = budgetData.value[key] || 0
      return {
        name: formatCategoryName(key),
        amount: `RM ${amount.toLocaleString()}`,
        percent: +(amount / total * 100).toFixed(1),
        color: categoryColors[key] || '#888888',
        key: key
      }
    })
    .filter(item => item.percent > 0)
    .sort((a, b) => b.percent - a.percent) // Sort by percentage descending
})

// Helper function to format category names
function formatCategoryName(key: string): string {
  const nameMap: Record<string, string> = {
    talent: 'Talent',
    location: 'Location',
    propsSet: 'Props & Set',
    wardrobeMakeup: 'Wardrobe & Makeup',
    sfxVfx: 'SFX & VFX',
    crew: 'Crew',
    miscellaneous: 'Miscellaneous'
  }
  
  return nameMap[key] || key
    .replace(/([A-Z])/g, ' $1')
    .replace(/^./, s => s.toUpperCase())
}

// Watch for project changes
watch(selectedProject, (newProject) => {
  if (newProject) {
    projectStore.setSelectedProject(newProject.title)
  }
}, { immediate: true })

// Load projects when component mounts
onMounted(async () => {
  console.log('BudgetView mounted, loading projects and scripts...')
  
  // Load both projects and scripts
  await Promise.all([
    projectStore.fetchProjects(),
    projectStore.fetchScripts()
  ])
  
  // Load budget data for initial project
  if (selectedProject.value) {
    await loadBudgetData()
  }
  
  // Set default project if none selected
  if (!selectedProjectTitle.value && projects.value.length > 0) {
    selectedProjectTitle.value = projects.value[0].title
    selectedProjectLocal.value = projects.value[0].title
  }
  
  console.log('BudgetView projects loaded:', projects.value.length)
  console.log('Selected project:', selectedProjectTitle.value)
  console.log('Selected project budget:', selectedProject.value?.scriptBreakdown?.budget)
})
</script>

<style scoped>
div[style*="linear-gradient"] {
  background: linear-gradient(90deg, #00C6FB 0%, #005BEA 100%) !important;
}
</style>
