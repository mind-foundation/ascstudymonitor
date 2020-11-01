module.exports = {
  theme: {
    extend: {},
    fontFamily: {
      sans: ['"Open Sans"', 'sans-serif'],
    },
    container: {
      center: true,
    },
    colors: {
      blue: '#76a1bb',
      superwhite: '#FFFFFF',
      white: '#EEF2F5', // contrast color
      black: '#00212b', // main font color
      red: '#AB0400', // danger color
      navy: '#0B2D3D', // secondary font color
      aqua: '#34557F', // link color disciplines
      danger: '#ab0400', // link color disciplines
      lightblue: '#6B97B2',
      gray: '#999',
      lightgrey: '#333',
    },
  },
  variants: {},
  plugins: [],
  purge: {
    enabled: process.env.NODE_ENV === 'production',
    content: ['./public/**/*.html', './src/**/*.vue'],
    options: {
      whitelistPatterns: [
        /-(leave|enter|appear)(|-(to|from|active))$/,
        /^(?!(|.*?:)cursor-move).+-move$/,
        /^router-link(|-exact)-active$/,
      ],
    },
  },
  future: {
    // remove after upgrading due vue-tailwind@2.0.0
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true,
  },
}
