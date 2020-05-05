/* Cache the database so that the visitor will never forget us */

const USE_CACHE = true // for development
const FAST_DEV = false // reduce data for fast development

const MIND_ASC_STORAGE_KEY_CACHE = 'mind-asc-cache'
const MIND_ASC_STORAGE_KEY_LAST = 'mind-asc-last'
const MIND_ASC_STORAGE_KEY_VERSION = 'mind-asc-version'
const CURRENT_VERSION = 2
const CACHE_EXPIRY_MS = 3600e3 // one hour

class Documents {
	transformData(data) {
		// add author labels
		data = data.map(d => ({
			...d,
			authorLabels: d.authors.map(a => `${a.first_name} ${a.last_name}`),
		}))
		return data
	}

	async cacheGood() {
		// check if cache good for use
		// check cache version
		const cacheVersion = await localforage.getItem(MIND_ASC_STORAGE_KEY_VERSION)
		if (cacheVersion !== CURRENT_VERSION) {
			this.clearAll()
			return false
		}

		// check expiration
		const lastDate = new Date(
			await localforage.getItem(MIND_ASC_STORAGE_KEY_LAST)
		)
		const msSinceLastAccess = +new Date() - lastDate
		console.info(
			'[Cache] Last stored %ss ago',
			Math.round(msSinceLastAccess / 1000)
		)
		if (msSinceLastAccess >= CACHE_EXPIRY_MS) {
			return false
		}

		return USE_CACHE
	}

	async fetch() {
		// fetch from remote
		console.info('[Cache] Need to refetch')
		let data = await $.getJSON('/documents.json')
		data = this.transformData(data)
		this.put(data)
		return data
	}

	async put(data) {
		// save to cache
		await localforage.setItem(MIND_ASC_STORAGE_KEY_CACHE, data)
		await localforage.setItem(
			MIND_ASC_STORAGE_KEY_LAST,
			new Date().toISOString()
		)
		await localforage.setItem(MIND_ASC_STORAGE_KEY_VERSION, CURRENT_VERSION)
	}

	async getFromCache() {
		// get data from cache
		const data = await localforage.getItem(MIND_ASC_STORAGE_KEY_CACHE)
		if (!data) {
			// even though cache was good, didnt get any data for some reason
			console.warn('[Cache] Need fetch even though cache is good')
			return this.fetch()
		}

		return data
	}

	async get() {
		// get the data from cache or fetch
		if (!USE_CACHE || FAST_DEV) {
			console.warn('[Cache] Dev mode active')
		}

		let data = null
		const cacheGood = await this.cacheGood()

		if (cacheGood) {
			data = await this.getFromCache()
			console.info('[Cache] Served %s entries from cache', data.length)
		} else {
			data = await this.fetch()
			console.info('[Cache] Served %s entries from remote', data.length)
		}

		if (FAST_DEV) {
			// for faster development
			data.length = 100
			data = data.filter(d => d.file_attached)
		}
		return data
	}

	async clearAll() {
		// clear legacy cache on local storage
		console.warn('[Cache] clearing cache')
		localStorage.clear()
		await localforage.clear()
	}
}
