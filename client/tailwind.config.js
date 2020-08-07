module.exports = {
  theme: {
    extend: {},
    fontFamily: {
      sans: ['"Open Sans"', 'sans-serif'],
    },
    colors: {
      blue: '#6B97B2',
      superwhite: '#FFFFFF',
      white: '#EEF2F5', // contrast color
      black: '#00212b', // main font color
      red: '#AB0400', // danger color
      navy: '#0B2D3D', // secondary font color
      lightblue: '#6B97B2',
      gray: '#C4D5E0',
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
}
