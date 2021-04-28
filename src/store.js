import { reactive } from 'vue'
import datasetsCode from './templates/datasets.py?raw'
import mainCode from './templates/main.py?raw'
import modelsCode from './templates/models.py?raw'
import readmeCode from './templates/README.md?raw'
import requirementsCode from './templates/requirements.txt?raw'
import trainersCode from './templates/trainers.py?raw'
import utilsCode from './templates/utils.py?raw'

export const store = reactive({
  config: {},
  generatedCode: Object.fromEntries(getTemplateFileNames().map((v) => [v, ''])),
})

export function saveConfig(key, value) {
  if (store.config[key] === undefined || store.config[key] !== value) {
    store.config[key] = value
  }
}

export function getTemplateFileNames() {
  return [
    'README.md',
    'config.json',
    'datasets.py',
    'main.py',
    'models.py',
    'trainers.py',
    'utils.py',
    'requirements.txt',
  ]
}

export function generateCode(currentTab) {
  const fileNames = getTemplateFileNames()
  const generateFnArray = [generateReadmeCode, generateConfigCode, generateDatasetsCode, generateMainCode, generateModelsCode, generateTrainersCode, generateUtilsCode, generateRequirementsCode]

  const index = fileNames.findIndex((value) => value === currentTab)
  return generateFnArray[index]().trim()
}


function generateConfigCode() {
  return JSON.stringify(store.config, null, 2)
}

function generateDatasetsCode() {
  return datasetsCode
}

function generateMainCode() {
  return mainCode
}

function generateModelsCode() {
  return modelsCode
}

function generateReadmeCode() {
  return readmeCode
}

function generateRequirementsCode() {
  return requirementsCode
}

function generateTrainersCode() {
  return trainersCode
}

function generateUtilsCode() {
  return utilsCode
}
