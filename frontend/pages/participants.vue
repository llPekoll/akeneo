<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">Participants</h2>
    <div class="mb-4">
      <form class="flex space-x-2" @submit.prevent="addParticipant">
        <input
          v-model="newParticipant.name"
          type="text"
          placeholder="Name"
          class="border p-2 rounded"
          required
        />
        <input
          v-model="newParticipant.email"
          type="email"
          placeholder="Email"
          class="border p-2 rounded"
          required
        />
        <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">
          Add
        </button>
      </form>
    </div>
    <ul class="divide-y divide-gray-200">
      <li
        v-for="participant in participants"
        :key="participant.id"
        class="py-4 flex justify-between"
      >
        <div>
          <p class="text-sm font-medium text-gray-900">
            {{ participant.name }}
          </p>
          <p class="text-sm text-gray-500">{{ participant.email }}</p>
        </div>
        <button
          class="text-red-600 hover:text-red-900"
          @click="removeParticipant(participant.id)"
        >
          Remove
        </button>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'ParticipantsPage',
  data() {
    return {
      participants: [],
      newParticipant: {
        name: '',
        email: '',
      },
    }
  },
  created() {
    this.fetchParticipants()
  },
  methods: {
    async fetchParticipants() {
      const response = await this.$axios.$get('participants/')
      this.participants.push(...response)
    },
    async addParticipant() {
      const response = await this.$axios.$post(
        'participants/',
        this.newParticipant
      )
      this.participants.push(response)
      this.newParticipant = { name: '', email: '' }
    },
    async removeParticipant(id) {
      await this.$axios.$delete(`participants/${id}/`)
      this.participants = this.participants.filter((p) => p.id !== id)
    },
  },
}
</script>
