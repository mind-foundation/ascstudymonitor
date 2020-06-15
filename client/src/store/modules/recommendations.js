import Vue from 'vue'
import { sampleSize } from 'lodash'
const log = require('debug')('store:recommendations')
log.enabled = true

const state = {
  items: {},
}

const mutations = {
  setRecommendation: (state, { id, recommendations }) => {
    log('setRecommendation %o %o', id, recommendations)
    Vue.set(state.items, id, recommendations)
  },
}

const actions = {
  get: (context, id) => {
    const recommendations = conjureRecommendations(id)
    setTimeout(() => {
      context.commit('setRecommendation', {
        id,
        recommendations,
      })
    }, 500 + 1000 * Math.random())
  },
}

const getters = {}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}

function conjureRecommendations(currentId) {
  return sampleSize(
    [
      '5c11faec-7dc8-3d70-8057-6388aaec0a9f',
      '9ae9d420-bb68-37e4-a612-20de9c018841',
      'd6a8f5cf-6bed-3cb9-a707-f0855d1a1532',
      'fed54968-46c0-36b8-be40-ec932f6464b3',
      '470157ed-d9ed-37a0-9a4f-2a942d687038',
      '045e444c-0b04-3b1c-8caf-008950df0d9a',
      'c27b4bb7-f8f9-314f-a1eb-03baca308a84',
      '3000b810-b8a8-3be4-9a5d-b9bda35220c1',
      '72cf023d-a697-318d-93d2-06681481019d',
      '143d8d5f-4a29-3577-83af-5f3b3c2486f9',
      '21968a8f-8f50-35d9-9579-5323ae4b4f3f',
      '21ed1a6e-7f00-3d27-a0d7-e6c32d445c7f',
      'bd21654d-92c5-3610-bddd-e54d92097cb1',
      '89c457f1-8540-328c-89f7-65e701ff8e1f',
      'db3da24e-2a7f-324b-a1be-c6bed3f4aea6',
      '5a886eb7-a20c-3926-b4b6-580e02ea5980',
      '2cd9c1a7-4475-35a6-8982-4276a33e709d',
      '6ae85a41-189e-3d22-8362-88d012e5331a',
      'f349d291-3d9c-30d4-ab72-664f2a0cd3cf',
      'd19b9411-0657-3238-8246-181ea0c7de15',
      'ea255a87-9abe-3384-8c41-121b297c6b34',
      '412bb499-9436-3958-b684-6c9fbf6fa2d3',
      '0e1c1260-7443-3307-905f-1aa2277af1d1',
      'e00837d8-d849-37dd-8cab-54d9192f31c4',
      'b1c54b47-dbea-3b52-8fdf-6616f0db600f',
      'df4835af-c7c8-3b6e-b486-89544f43b4b5',
      '51fe2946-6e4b-3cf9-a115-844fd470c7ae',
      '75ecaf3d-b858-396a-b238-7e21debcecbf',
      '114a16ae-cc0d-30e8-9cf7-4fc13d4255bb',
      '208254a4-bcfb-31b7-ad17-a1fb53eb1dcc',
      'fd005409-758d-36ad-8208-7b2656548080',
      'e3e59192-9591-3de2-b0db-73c9e8f6c633',
      '2acdb109-095c-381e-a2b8-2fff3e9330ad',
      '5fb03ad3-6df5-3fbe-8bce-171b4b1b753a',
      '2397d476-fb88-3af8-82b3-089cebb6b814',
      'd10b7227-d620-3b33-9926-ee717e546373',
      '4e8a427c-bd97-3845-be80-00e58610b3f1',
      '9d00e066-94d5-3e0d-8bc6-b4aa3a2fb031',
      '7383bed3-2a35-36d5-84fe-66c639ea5d03',
      'ece2347c-51b3-3d32-b91a-5927bc7d264e',
      '38f6f79b-6f97-3bfc-9998-a72d4dd58b89',
      '796e6e8c-3c75-31ec-a0d1-2a4aa5af3520',
      '8527eab3-3a26-3e65-b6b5-ab6f58caf576',
      'bf30cbee-aab9-385d-a794-1363dca5a6a6',
      '877d32b5-63da-3959-8d5f-87b987e44ead',
      'bf6a8176-11b5-3ad9-80b9-855b43c5bda4',
    ].filter(id => id !== currentId),
    2,
  )
}
