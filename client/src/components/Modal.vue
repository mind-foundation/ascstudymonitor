<script>
export default {
  name: 'modal',
}
</script>

<template>
  <transition name="modal">
    <div class="modal-mask">
      <div class="modal-wrapper" @click="$emit('close')">
        <div class="modal-container reveal" @click.stop>
          <h3>Thank you for being here</h3>

          <div class="modal-body">
            <p>
              The ASC Study Monitor is a curated, freely accessible, and
              regularly updated database of scholarly publications concerning
              altered states of consciousness (ASCs). The publications included
              in the ASC Study Monitor mainly cover the field of the “mind &
              brain sciences” including philosophy, psychology, psychiatry,
              neuroscience, and medicine as well as natural sciences. Moreover,
              the monitor covers relevant publications from cultural studies and
              the social sciences that discuss altered states of consciousness.
              With the ASC Study Monitor, MIND provides a multidisciplinary
              reference base to researchers, practitioners, students, and the
              interested public. This aims to enable high-quality,
              evidence-based public discussions of consciousness, its
              alterations, capabilities, and pathologies.
            </p>
            <p>
              Visit the MIND website for more information and ways to support
              this project.
            </p>
            <div>
              <a
                href="https://mind-foundation.org/project/asc-study-monitor?utm_source=asc-studymonitor&utm_medium=info-popup"
                target="_blank"
              >
                Go to the MIND website
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<style lang="less" scoped>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: table;
  transition: opacity 0.3s ease;
}

.modal-wrapper {
  display: table-cell;
  vertical-align: middle;
}

.modal-container {
  width: 600px;
  margin: 0px auto;
  background-color: #fefefe;
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
  transition: all 0.3s ease;
  font-family: Helvetica, Arial, sans-serif;

  h3 {
    margin-top: 0;
    color: #42b983;
    font-size: 1.9375rem;
  }
}

.modal-body {
  margin: 10px 0;
}

.modal-default-button {
  float: right;
}

.reveal {
  text-align: left;
  padding: 30px 45px;
  position: relative;
  outline: none;

  h3 {
    text-align: left;
    color: #333;
    font-weight: 300;
  }

  p {
    margin: 0;
    text-align: left;
    color: #333;
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

/*
 * The following styles are auto-applied to elements with
 * transition="modal" when their visibility is toggled
 * by Vue.js.
 *
 * You can easily play with the modal transition by editing
 * these styles.
 */

.modal-enter {
  opacity: 0;
}

.modal-leave-active {
  opacity: 0;
}

.modal-enter .modal-container,
.modal-leave-active .modal-container {
  -webkit-transform: scale(1.1);
  transform: scale(1.1);
}
</style>
