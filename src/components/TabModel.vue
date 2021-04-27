<template>
  <div class="tab-model">
    <div class="domain">
      <label for="domain-select">Domain:</label>
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
      <label for="subdomain-select">{{ selectedDomain }} Sub Domains:</label>
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
      <label for="model-select"
        >{{ selectedSubDomain }} Available Models:</label
      >
      <select
        name="model"
        id="model-select"
        v-model="selectedModel"
        @change="saveConfig"
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
  </div>
</template>

<script>
import vision from '../metadata/models/vision.json'
import text from '../metadata/models/text.json'
import { saveConfig } from '../store'

export default {
  data() {
    return {
      urls: {
        Vision: 'https://pytorch.org/vision/stable/models.html',
        Text: '',
        Audio: ''
      },
      domainsObj: { Vision: vision, Text: text, Audio: {} },
      selectedDomain: '',
      selectedSubDomain: '',
      selectedModel: ''
    }
  },
  computed: {
    domainChange() {
      if (this.selectedSubDomain) {
        this.selectedSubDomain = ''
        this.selectedModel = ''
      }
    },
    subDomainChange() {
      if (this.selectedModel) {
        this.selectedModel = ''
      }
    },
    saveConfig() {
      const subDomainModel = {}
      subDomainModel[this.selectedSubDomain.toLowerCase()] = this.selectedModel
      saveConfig(this.selectedDomain.toLowerCase(), subDomainModel)
    }
  }
}
</script>

<style scoped>
.tab-model {
  margin: 1.5rem 2.5rem;
}
.domain {
  padding: 1rem;
}
.subdomain {
  padding: 1rem;
}
.model {
  padding: 1rem;
}
</style>
