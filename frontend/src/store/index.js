import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    loaded: false,
    publications: [],
  },
  mutations: {
    MUTATE_PUBLICATIONS: (state, publications) => {
      publications = publications.map(pub => ({
        ...pub,
        authorNames: pub.authors.map(a => `${a.first_name} ${a.last_name}`),
      }))
      Vue.set(state, 'publications', publications)
      Vue.set(state, 'loaded', true)
    },
  },
  actions: {
    loadPublications: context => {
      setTimeout(() => {
        console.log('!timer')
        context.commit('MUTATE_PUBLICATIONS', getSample())
      }, 30000)
      fetch('http://localhost:5000/documents.json')
        .then(res => res.json())
        .then(function(data) {
          context.commit('MUTATE_PUBLICATIONS', data)
        })
    },
    loadPublication: () => {
      // fetch('http://localhost:5000/documents.json')
      //   .then(res => res.json())
      //   .then(function(data) {
      //     context.commit('MUTATE_PUBLICATIONS', data)
      //   })
    },
  },
  modules: {},
  getters: {
    getPublications: state => state.publications,
  },
})

function getSample() {
  return [
    {
      abstract:
        'Ibogaine is an alkaloid purported to be an effective drug dependence treatment. However, its efficacy has been hard to evaluate, partly because it is illegal in some countries. In such places, treatments are conducted in underground settings where fatalities have occurred. In Brazil ibogaine is unregulated and a combined approach of psychotherapy and ibogaine is being practiced to treat addiction. To evaluate the safety and efficacy of ibogaine, we conducted a retrospective analysis of data from 75 previous alcohol, cannabis, cocaine and crack users (72% poly-drug users). We observed no serious adverse reactions or fatalities, and found 61% of participants abstinent. Participants treated with ibogaine only once reported abstinence for a median of 5.5 months and those treated multiple times for a median of 8.4 months. This increase was statistically significant (p < 0.001), and both single or multiple treatments led to longer abstinence periods than before the first ibogaine session (p < 0.001). These results suggest that the use of ibogaine supervised by a physician and accompanied by psychotherapy can facilitate prolonged periods of abstinence, without the occurrence of fatalities or complications. These results suggest that ibogaine can be a safe and effective treatment for dependence on stimulant and other non-opiate drugs.',
      authors: [
        {
          first_name: 'Eduardo Ekman',
          last_name: 'Schenberg',
        },
        {
          first_name: 'Maria Angélica',
          last_name: 'De Castro Comis',
        },
        {
          first_name: 'Bruno Rasmussen',
          last_name: 'Chaves',
        },
        {
          first_name: 'Dartiu Xavier',
          last_name: 'Da Silveira',
        },
      ],
      created: '2017-11-10T18:19:02.497Z',
      disciplines: ['testdiscipline A'],
      file_attached: false,
      id: '205ebd9f-678c-32fd-af41-170736ec2111',
      source: 'Journal of Psychopharmacology',
      title:
        'Treating drug dependence with the aid of ibogaine: A retrospective study',
      websites: ['http://www.akademiai.com/doi/abs/10.1556/2054.01.2016.002'],
      year: 2014,
    },
    {
      abstract:
        'Cluster headache is a highly disabling primary headache disorder, characterized by unilateral headache attacks occurring in association with cranial autonomic symptoms. Serotonergic agents, such as the ergot alkaloids, have traditionally been used for the acute and preventive treatment of cluster headache and other primary headaches. Although it initially was thought that their efficacy was due solely to the vasoconstriction of extracranial cerebral vessels, new mechanisms of action of these drugs have been ascertained as a consequence of advances in elucidation of the pathogenesis of primary headaches and the development of triptans. This article reviews the current knowledge about serotonergic agonists and antagonists used in the management of cluster headache, focusing on their mechanisms of action and on the possible role of serotonin system dysfunction in this complex disorder.',
      authors: [
        {
          first_name: 'Giorgio',
          last_name: 'Lambru',
        },
        {
          first_name: 'Manjit',
          last_name: 'Matharu',
        },
      ],
      created: '2017-11-10T18:19:02.496Z',
      disciplines: ['testdiscipline A', 'testdiscipline B'],
      file_attached: false,
      id: 'b4771194-12d5-3059-8953-2dde0516eb4a',
      source: 'Current Pain and Headache Reports',
      title: 'Serotonergic agents in the management of cluster headache',
      year: 2011,
    },
  ]
}
