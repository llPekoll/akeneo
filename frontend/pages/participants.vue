<template>
  <div class="p-4">
    <h2 class="text-2xl font-bold mb-4">Participants</h2>

    <!-- Add Participant Form -->
    <div class="mb-4 p-4 border rounded">
      <h3 class="text-lg font-semibold mb-2">Add Participant</h3>
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

    <!-- Add to Blacklist Form -->
    <div class="mb-4 p-4 border rounded">
      <h3 class="text-lg font-semibold mb-2">Add to Blacklist</h3>
      <form class="flex space-x-2" @submit.prevent="addBlacklist">
        <select
          v-model="newBlacklist.participantId"
          class="border p-2 rounded"
          required
        >
          <option value="">Select Participant</option>
          <option
            v-for="participant in participants"
            :key="participant.id"
            :value="participant.id"
          >
            {{ participant.name }}
          </option>
        </select>
        <input
          v-model="newBlacklist.email"
          type="email"
          placeholder="Blacklist Email"
          class="border p-2 rounded"
          required
        />
        <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">
          Add to Blacklist
        </button>
      </form>
    </div>

    <!-- Participants List -->
    <ul class="space-y-4">
      <li
        class="border-b-2"
        v-for="participant in participants"
        :key="participant.id"
      >
        <div class="flex justify-between items-center mb-2">
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
        </div>
        <div>
          <h4 class="text-sm font-medium text-gray-900 mb-1">Blacklist:</h4>
          <ul class="text-sm text-gray-500">
            <li
              v-for="email in participant.blacklist"
              :key="email"
              class="flex justify-between items-center"
            >
              {{ email }}
            </li>
          </ul>
        </div>
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
      blacklist: [],
      newParticipant: {
        name: '',
        email: '',
      },
      newBlacklist: {
        participantId: '',
        email: '',
      },
    }
  },
  created() {
    this.fetchParticipants()
    this.fetchBlacklist()
  },
  methods: {
    async fetchParticipants() {
      try {
        const response = await this.$axios.$get('participants/')
        this.participants = response.map((p) => ({
          ...p,
          blacklist: p.blacklist || [],
        }))
      } catch (error) {
        console.error('Error fetching participants:', error)
      }
    },
    async fetchBlacklist() {
      try {
        const response = await this.$axios.$get('blacklists/')
        this.blacklist = response
        this.participants.forEach((participant) => {
          participant.blacklist = this.blacklist.filter(
            (entry) => entry.blocked_participant === participant.id
          ).map((entry) => entry.participant_email)
        })
      } catch (error) {
        console.error('Error fetching blacklist:', error)
      }
    },
    async addParticipant() {
      try {
        const response = await this.$axios.$post(
          'participants/',
          this.newParticipant
        )
        this.participants.push({ ...response, blacklist: [] })
        this.newParticipant = { name: '', email: '' }
      } catch (error) {
        console.error('Error adding participant:', error)
      }
    },
    async removeParticipant(id) {
      try {
        await this.$axios.$delete(`participants/${id}/`)
        this.participants = this.participants.filter((p) => p.id !== id)
      } catch (error) {
        console.error('Error removing participant:', error)
      }
    },
    async addBlacklist() {
      try {
        const participant = this.participants.find(
          (p) => p.id === parseInt(this.newBlacklist.participantId)
        )
        if (!participant) return

        await this.$axios.$post(`blacklists/`, {
          participant_email: this.newBlacklist.email,
          blocked_participant: this.newBlacklist.participantId,
        })
        participant.blacklist.push(this.newBlacklist.email)
        this.newBlacklist = { participantId: '', email: '' }
      } catch (error) {
        console.error('Error adding to blacklist:', error)
      }
    },
  },
}
</script>
