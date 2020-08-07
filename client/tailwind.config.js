module.exports = {
  theme: {
    extend: {},
    fontFamily: {
      sans: ['"Open Sans"', 'sans-serif'],
    },
    colors: {
      blue: '#6B97B2',
      white: '#EEF2F5',
      red: 'red',
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
