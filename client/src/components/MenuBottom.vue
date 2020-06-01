<script>
import Modal from './Modal'

export default {
  name: 'icon-author',
  components: { Modal },
  data: () => ({
    showModal: false,
  }),
}
</script>

<template>
  <div id="menu-bottom">
    <a @click="showModal = true">Info</a>
    <div v-if="showModal">
      <modal @close="showModal = false" />
    </div>
    <div id="menu-about">
      <p>
        <span class="menu-bottom__asc">ASC</span>
        <span class="menu-bottom__study-monitor">Study Monitor</span>
      </p>
      <span class="menu-bottom__love">
        Made with &hearts; in Berlin
      </span>
    </div>
  </div>
</template>

<style lang="less" scoped>
#menu-bottom {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: stretch;
  text-align: center;

  a {
    color: #fff;
    font-size: 11pt;
    display: inline-block;

    margin: 0 auto;
    padding: 10px;
    cursor: pointer;
    opacity: 0.9;

    &:focus {
      outline: none;
    }

    &:hover {
      opacity: 1;
    }
  }
}

#menu-about {
  border-top: 1px solid rgba(255, 255, 255, 0.15);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  height: 70px;
}

#menu-bottom p {
  display: inline;
  margin: 0 0 2px 0;
  font-size: 1.2em;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.menu-bottom__asc {
  font-weight: 700;
  letter-spacing: 0.15em;
  display: inline-block;
  margin-right: 3px;
}

.menu-bottom__study-monitor {
  letter-spacing: 0.04em;
  font-weight: 300;
}
.menu-bottom__love {
  display: block;
  font-size: 0.8em;
  font-weight: 700;
}
</style>
