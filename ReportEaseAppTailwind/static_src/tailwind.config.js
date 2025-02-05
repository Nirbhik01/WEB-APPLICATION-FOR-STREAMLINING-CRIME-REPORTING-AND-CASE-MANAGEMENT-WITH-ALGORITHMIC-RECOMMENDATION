/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        colors: {
            "dark-blue": "#2C3E50",
            "white": "#ffffff",
            "black": "#000000",
            "cool-gray": "#95A5A6",
            "light-gray": "#f2f0ef",
            "gray": "#d3d3d3",
            "dark-yellow": "#edaf28",
        },
        extend: {
            backgroundImage: {
                'Homepage-bcg': "url('/static/ReportEaseApp/Homepage/image.png')",

            },

            animation: {
                blink: 'blink 1.4s infinite both',
                fade: 'fade 1.4s infinite both',
                scale: 'scale 1.5s infinite',
                perspective: 'perspective 1.2s infinite',
                fadeIn: 'fadeIn 1.2s ease-in-out infinite both',
            },
            keyframes: {
                blink: {
                    '0%': {
                        opacity: '0.2',
                    },
                    '20%': {
                        opacity: '1',
                    },
                    '100%': {
                        opacity: ' 0.2',
                    },
                },
                fade: {
                    '0%, 100%': {
                        opacity: '1',
                    },
                    '50%': {
                        opacity: ' 0.3',
                    },
                },
                fadeIn: {
                    '0%, 39%, 100%': {
                        opacity: '0',
                    },
                    '40%': {
                        opacity: '1',
                    },
                },
                scale: {
                    '0%, 100%': {
                        transform: 'scale(1.0)',
                    },
                    '50%': {
                        transform: 'scale(0.7)',
                        // change this to set how small you want the element to shrink
                    },
                },
                perspective: {
                    '0%': { transform: 'perspective(120px)' },
                    ' 50%': { transform: 'perspective(120px) rotateY(180deg)' },
                    '100%': { transform: 'perspective(120px) rotateY(180deg)  rotateX(180deg)' },
                },
            },
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),

        // !!!! This plugin should be copied for all loading spinners !!!!
        // plugin (({ matchUtilities, theme }) => {
        //     matchUtilities(
        //         {
        //             'animation-delay': (value) => {
        //                 return {
        //                     'animation-delay': value,
        //                 }
        //             },
        //         },
        //         {
        //             values: theme('transitionDelay'),
        //         }
        //     )
        // }),
    ],
}
