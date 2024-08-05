<template>
  <div class="min-h-screen bg-gray-100">
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <NuxtLink to="/" class="text-2xl font-bold text-indigo-600"
                >Secret Santa</NuxtLink
              >
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <NuxtLink
                to="/"
                class="border-indigo-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              >
                Home
              </NuxtLink>
              <NuxtLink
                to="/participants"
                class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              >
                Participants
              </NuxtLink>
              <NuxtLink
                to="/draw"
                class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              >
                Draw
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <div class="py-10">
      <main>
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
          <Nuxt />
        </div>
      </main>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DefaultLayout',
}
</script>
