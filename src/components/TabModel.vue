<template>
  <div class="tab-model">
    <h1>Model Selection</h1>
    <div class="domain">
      <h2><label for="domain-select">Domain:</label></h2>
      <select
        name="domain"
        id="domain-select"
        v-model="selectedDomain"
        @change="domainChange"
      >
        <option disabled value="">--- Please select an option ---</option>
        <option
          :value="domain"
          :key="index"
          v-for="(domain, index) of Object.keys(domainsObj)"
        >
          {{ domain }}
        </option>
      </select>
    </div>
    <div class="subdomain" v-if="selectedDomain">
      <h3>
        <label for="subdomain-select">{{ selectedDomain }} Sub Domains:</label>
      </h3>
      <select
        name="subdomain"
        id="subdomain-select"
        v-model="selectedSubDomain"
        @change="subDomainChange"
      >
        <option disabled value="">--- Please select a subdomain ---</option>
        <option
          :value="subDomain"
          :key="index"
          v-for="(subDomain, index) of Object.keys(domainsObj[selectedDomain])"
        >
          {{ subDomain }}
        </option>
      </select>
    </div>
    <div class="model" v-if="selectedSubDomain">
      <h4>
        <label for="model-select"
          >{{ selectedSubDomain }} Available Models:</label
        >
      </h4>
      <select
        name="model"
        id="model-select"
        v-model="selectedModel"
        @change="saveModel"
      >
        <option disabled value="">--- Please select a model ---</option>
        <option
          :value="model"
          :key="index"
          v-for="(model, index) in domainsObj[selectedDomain][
            selectedSubDomain
          ]"
        >
          {{ model }}
        </option>
      </select>
    </div>
    <a
      class="learn-more"
      target="_blank"
      rel="noopener noreferrer"
      :href="urls[selectedDomain]"
      v-show="selectedDomain"
      >Learn more about available {{ selectedDomain }} models.</a
    >
  </div>
</template>

<script>
import vision from '../metadata/models/vision.json'
import text from '../metadata/models/text.json'
import { saveConfig } from '../store'
import { computed, ref } from 'vue'

export default {
  setup() {
    const selectedDomain = ref('')
    const selectedSubDomain = ref('')
    const selectedModel = ref('')
    const domainsObj = { Vision: vision, Text: text, Audio: {} }
    const urls = {
      Vision: 'https://pytorch.org/vision/stable/models.html',
      Text: '',
      Audio: ''
    }

    // computed properties
    const domainChange = computed(() => {
      if (selectedSubDomain.value) {
        selectedSubDomain.value = ''
        selectedModel.value = ''
      }
    })
    const subDomainChange = computed(() => {
      if (selectedModel.value) {
        selectedModel.value = ''
      }
    })
    const saveModel = computed(() => {
      const subDomainModel = {}
      subDomainModel[selectedSubDomain.value.toLowerCase()] =
        selectedModel.value
      saveConfig(selectedDomain.value.toLowerCase(), subDomainModel)
    })

    return {
      selectedDomain,
      selectedSubDomain,
      selectedModel,
      domainsObj,
      urls,
      domainChange,
      subDomainChange,
      saveModel
    }
  }
}
</script>

<style scoped>
.tab-model {
  margin: 0 1.5rem;
}
.domain,
.subdomain,
.model {
  position: relative;
}
.domain h2 {
  margin-bottom: 0;
}
.subdomain h3 {
  margin-bottom: 0.25rem;
}
.model h4 {
  margin-bottom: 0.5rem;
}
.domain select,
.subdomain select,
.model select {
  appearance: none;
  background: var(--c-white-light);
  border-radius: 3px;
  color: var(--c-text);
  cursor: pointer;
  font-family: var(--font-family-base);
  font-size: var(--font-size);
  padding: 0.5rem 1rem;
  text-align: center;
  width: 100%;
}
.domain::after,
.subdomain::after,
.model::after {
  content: '';
  position: absolute;
  right: 1rem;
  bottom: 16px;
  border-top: 6px solid var(--c-brand-red);
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-bottom: 0;
  vertical-align: middle;
}
.learn-more {
  display: block;
  margin-top: 1rem;
  max-width: max-content;
  font-weight: bold;
  text-transform: capitalize;
  text-decoration: none;
  border-bottom: 2px solid var(--c-brand-red);
  color: var(--c-text);
}
.learn-more:hover {
  border-bottom-color: transparent;
}
</style>
