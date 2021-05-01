import { reactive } from 'vue'
import datasets from './templates/datasets.py?raw'
import main from './templates/main.py?raw'
import models from './templates/models.py?raw'
import readme from './templates/README.md?raw'
import requirements from './templates/requirements.txt?raw'
import trainers from './templates/trainers.py?raw'
import utils from './templates/utils.py?raw'
import patch from './templates/_patch.py?raw'

export const store = reactive({
  config: {},
  _config: {},
  code: Object.fromEntries(getTemplateFileNames().map((v) => [v, '']))
})

export function saveConfig(key, value) {
  if (store._config[key] === undefined || store._config[key] !== value) {
    store._config[key] = value
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
  // model tab
  const subDomains = ['vision', 'text', 'audio']
  let validSubDomain
  const found = subDomains.some((value) => {
    validSubDomain = value
    return Object.keys(store._config).includes(value)
  })
  if (found) {
    const modelObj = store._config[validSubDomain]
    const key = Object.keys(modelObj)
    store.config['model'] = modelObj[key[0]]
  }
  for (const key of ['filename_prefix', 'dirname', 'n_saved']) [
    store.config[key] = store._config[key]
  ]
  return JSON.stringify(store.config, null, 2)
}

function generateDatasets() {
  return datasets
}

function generateMain() {
  const hasToSave = store._config.to_save
  store.code['main.py'] = main
  let toSaveCode = 'to_save = { '
  if (hasToSave) {
    for (const key in hasToSave) {
      if (hasToSave[key]) {
        toSaveCode += `'${key}': ${key}, `
      }
    }
    toSaveCode += '}'
    toSaveCode += '\n    handler = checkpoint_training(to_save, config)'
    store.code['main.py'] = main.replaceAll('# checkpoint_training', toSaveCode)
  }
  return store.code['main.py'] 
}

function generateModels() {
  const visionModel = store._config['vision']
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
  const launch = 'python -m torch.distributed.launch'
  const nproc_per_node = store._config.nproc_per_node
  const nnodes = store._config.nnodes
  const master_addr = store._config.master_addr
  const master_port = store._config.master_port
  let tempReadme = readme
  const cmdRegex = /python.*main.py/gi

  // multi processes
  if (nproc_per_node && nproc_per_node > 1) {
    // single node
    if (nnodes === 1 || !nnodes) {
      tempReadme = readme.replaceAll(
        cmdRegex,
        launch + ` --nproc_per_node ${nproc_per_node} main.py`
      )
    }
    // multi node
    if (nnodes && nnodes > 1) {
      const multinode =
        ` --nproc_per_node ${nproc_per_node}` +
        ` --nnodes ${nnodes}` +
        ` --master_addr ${master_addr}` +
        ` --master_port ${master_port}` +
        ' main.py'

      tempReadme = readme.replaceAll(cmdRegex, launch + multinode)
    }
  }
  store.code['README.md'] = tempReadme
  return store.code['README.md']
}

function generateRequirements() {
  return requirements
}

function generateTrainers() {
  if (store._config['deterministic']) {
    return trainers.replaceAll('Engine', 'DeterministicEngine')
  }
  return trainers
}

function generateUtils() {
  const hasToSave = store._config.to_save
  let tempCode = utils
  let patchCode
  if (hasToSave) {
    if (Object.values(hasToSave).some((value) => value === true)) {
      tempCode = utils.split('###')
      patchCode = patch.split('###\n')
      tempCode[1] += patchCode[1]
      tempCode.push(patchCode[2])
      tempCode = tempCode.join('\n')
    }
  }
  store.code['utils.py'] = tempCode
  return store.code['utils.py']
}
