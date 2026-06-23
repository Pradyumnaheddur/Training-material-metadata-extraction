<template>
  <div class="min-h-full flex flex-col bg-gray-50">
    <!-- Hero Section: two matching cards -->
    <section class="shrink-0 pt-5 pb-8 sm:pt-6 sm:pb-10">
      <div class="container-custom">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8 items-stretch">
          <!-- Left card: About DiscoRSE -->
          <Card padding="pt-4 px-5 pb-6 sm:pt-5 sm:px-6 sm:pb-7" custom-class="rounded-xl flex flex-col">
            <h1 class="text-xl sm:text-2xl font-bold text-secondary-800 tracking-tight mb-2.5">
              About DiscoRSE
            </h1>
            <p class="text-gray-600 text-sm sm:text-base leading-relaxed mb-4">
              <a
                href="https://www.discorse.de/"
                target="_blank"
                rel="noopener noreferrer"
                class="font-medium text-primary-700 hover:text-primary-800 underline-offset-2 hover:underline"
              >DiscoRSE</a>
              improves how Research Software Engineering open educational resources are found and used. RSE training materials are scattered across many sites with no central directory — the project builds a community-defined metadata schema and OER catalog for topic search, learning pathways, author visibility, and accessibility.
            </p>
            <p class="text-gray-600 text-sm sm:text-base leading-relaxed mb-4">
              This tool extracts metadata from code repositories in line with that schema, so training materials can be described consistently and discovered more easily.
              <a
                href="https://www.discorse.de/news/2025-02-19_what-is-discorse/"
                target="_blank"
                rel="noopener noreferrer"
                class="text-primary-600 hover:text-primary-700 underline underline-offset-1"
              >Learn more</a>
            </p>
            <NuxtLink
              to="/dashboard"
              class="btn btn-primary inline-flex items-center gap-2 w-fit"
            >
              Get Started
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </NuxtLink>
          </Card>

          <!-- Right card: same style as left -->
          <div class="w-full min-h-[200px]">
            <PlatformCarousel v-model="currentPlatform" :platforms="platforms" />
          </div>
        </div>
      </div>
    </section>

    <!-- Extraction pipeline: same width as About + Integrated Platforms above -->
    <section class="flex-1 flex flex-col justify-center pb-8 sm:pb-10">
      <div class="container-custom w-full">
        <ExtractionPipeline />
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

useHead({
  title: 'DiscoRSE - Describe your RSE open educational resources',
  meta: [
    {
      name: 'description',
      content:
        'Extract metadata from training material repositories for the DiscoRSE project — improving discoverability of RSE open educational resources.',
    },
  ],
})

const currentPlatform = ref(0)

const platforms = [
  {
    name: 'GitHub',
    logo: '/Github_logo.png',
    active: true,
  },
  {
    name: 'GitLab',
    logo: '/Gitlab_logo.png',
    active: true,
  },
  {
    name: 'Codeberg',
    logo: '/Codeberg_logo.png',
    active: false,
  },
]
</script>
