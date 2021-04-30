import { reactive } from 'vue'
import datasets from './templates/datasets.py?raw'
import main from './templates/main.py?raw'
import models from './templates/models.py?raw'
import readme from './templates/README.md?raw'
import requirements from './templates/requirements.txt?raw'
import trainers from './templates/trainers.py?raw'
import utils from './templates/utils.py?raw'

export const store = reactive({
  config: {},
  generatedCode: Object.fromEntries(getTemplateFileNames().map((v) => [v, '']))
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
    'requirements.txt'
  ]
}

export function generateCode(currentTab) {
  const fileNames = getTemplateFileNames()
  const generateFnArray = [
    generateReadme,
    generateConfig,
    generateDatasets,
    generateMain,
    generateModels,
    generateTrainers,
    generateUtils,
    generateRequirements
  ]

  const index = fileNames.findIndex((value) => value === currentTab)
  return generateFnArray[index]().trim()
}

function generateConfig() {
  return JSON.stringify(store.config, null, 2)
}

function generateDatasets() {
  return datasets
}

function generateMain() {
  return main.replaceAll(/###\s\w+\n/gi, '')
}

function generateModels() {
  const visionModel = store.config['vision']
  let modelsCode = ''

  if (visionModel) {
    const subDomain = Object.keys(visionModel)
    if (!subDomain.includes('classification')) {
      modelsCode = models.replaceAll(
        'models.__dict__',
        `models.${subDomain.toString()}.__dict__`
      )
    }
  } else {
    modelsCode = models
  }
  return modelsCode
}

function generateReadme() {
  return readme
}

function generateRequirements() {
  return requirements
}

function generateTrainers() {
  if (store.config['deterministic']) {
    return trainers.replaceAll('Engine', 'DeterministicEngine')
  }
  return trainers
}

function generateUtils() {
  return utils.replaceAll(/###\s\w+\n/gi, '')
}
