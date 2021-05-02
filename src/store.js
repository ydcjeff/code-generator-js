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
  _config: {},
  code: {}
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
  for (const key of ['filename_prefix', 'dirname', 'n_saved']) {
    store.config[key] = store._config[key]
  }
  store.code['config.json'] = JSON.stringify(store.config, null, 2)
  return store.code['config.json']
}

function generateDatasets() {
  store.code['datasets.py'] = datasets
  return store.code['datasets.py']
}

function generateMain() {
  const hasToSave = store._config.to_save
  store.code['main.py'] = main
  if (hasToSave) {
    let to_save_train = ''
    for (const key in hasToSave) {
      if (hasToSave[key]) {
        to_save_train += `'${key}': ${key}, `
      }
    }

    let toSaveCode = `to_save_train = { ${to_save_train} }
    to_save_eval = { 'model': model }
    ckpt_handler_train, ckpt_handler_eval = checkpointing(to_save_train, to_save_eval, config)`
    store.code['main.py'] = main.replaceAll('# checkpointing', toSaveCode)
  }
  return store.code['main.py']
}

function generateModels() {
  const visionModel = store._config['vision']
  let modelsCode = models

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
  store.code['models.py'] = modelsCode
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
        launch + ` --nproc_per_node ${nproc_per_node} main.py --backend nccl`
      )
    }
    // multi node
    if (nnodes && nnodes > 1) {
      const multinode =
        ` --nproc_per_node ${nproc_per_node}` +
        ` --nnodes ${nnodes}` +
        ` --master_addr ${master_addr}` +
        ` --master_port ${master_port}` +
        ' main.py --backend nccl'

      tempReadme = readme.replaceAll(cmdRegex, launch + multinode)
    }
  }
  store.code['README.md'] = tempReadme
  return store.code['README.md']
}

function generateRequirements() {
  store.code['requirements.txt'] = requirements
  return store.code['requirements.txt']
}

function generateTrainers() {
  store.code['trainers.py'] = trainers
  if (store._config['deterministic']) {
    store.code['trainers.py'] = trainers.replaceAll(
      'Engine',
      'DeterministicEngine'
    )
  }
  return store.code['trainers.py']
}

function generateUtils() {
  const hasToSave = store._config.to_save
  let tempCode = utils.split('### ')
  tempCode = Object.fromEntries(tempCode.map((value) => value.split(' ###')))
  if (hasToSave) {
    if (Object.values(hasToSave).every((value) => value === false)) {
      delete tempCode.checkpointing
    }
  } else {
    delete tempCode.checkpointing
  }
  store.code['utils.py'] = Object.values(tempCode).join('')
  return store.code['utils.py']
}
