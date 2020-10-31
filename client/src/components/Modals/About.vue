<script>
export default {
  name: 'about-modal',
  methods: {
    beforeOpen() {
      window.analytics.page('Modal.About')
    },
  },
}
</script>

<template>
  <modal
    name="about-modal"
    :width="600"
    :height="430"
    @before-open="beforeOpen"
  >
    <div class="container modal-container bg-superwhite p-6">
      <h3 class="text-navy text-3xl mb-3">Thank you for being here</h3>

      <p class="leading-6 mb-6">
        The ASC Study Monitor is a curated, freely accessible, and regularly
        updated database of scholarly publications concerning altered states of
        consciousness (ASCs). The publications included in the ASC Study Monitor
        mainly cover the field of the “mind &amp; brain sciences” including
        philosophy, psychology, psychiatry, neuroscience, and medicine as well
        as natural sciences. Moreover, the monitor covers relevant publications
        from cultural studies and the social sciences that discuss altered
        states of consciousness. With the ASC Study Monitor, MIND provides a
        multidisciplinary reference base to researchers, practitioners,
        students, and the interested public. This aims to enable high-quality,
        evidence-based public discussions of consciousness, its alterations,
        capabilities, and pathologies.
      </p>

      <div class="text-center">
        <p class="italic mb-2">
          Visit the MIND website for more information and ways to support this
          project.
        </p>
        <p>
          <a
            href="https://mind-foundation.org/research/a-s-c-monitor?utm_source=asc-studymonitor&utm_medium=about-popup"
            target="_blank"
          >
            <button
              class="pt-3 pb-3 pl-10 pr-10 leading-none bg-navy hover:bg-danger hover:pl-12 hover:pr-12 bg-transparent text-white text-xs font-bold uppercase"
            >
              Go to the MIND website
            </button>
          </a>
        </p>
        <p class="mt-2">
          Made with ♥️ in Berlin
        </p>
      </div>
    </div>
  </modal>
</template>

<style>
.modal-container {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  height: 100%;
}

button {
  transition: all 0.2s ease-in-out;
}

/*
.reveal {
  text-align: left;
  padding: 30px 45px;
  position: relative;
  outline: none;

  h3 {
    text-align: left;
    font-weight: 300;
  }

  p {
    margin: 0;
    text-align: left;
    line-height: 1.8;
    padding-bottom: 20px;
  }

  a {
    font-weight: 600;
    color: #fff;
    background: linear-gradient(to right, #1a9da4, #34557f);
    padding: 3px 20px;
    font-size: 15px;
    line-height: 3em;
    display: inline-block;
  }
}
*/
</style>
