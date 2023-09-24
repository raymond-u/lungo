import adapter from "@sveltejs/adapter-static"
import { vitePreprocess } from "@sveltejs/kit/vite"

export default {
    preprocess: [vitePreprocess({})],
    kit: {
        adapter: adapter({
            // default options are shown. On some platforms
            // these options are set automatically — see below
            pages: "../src/lungo_cli/res/www",
            assets: "../src/lungo_cli/res/www",
            fallback: undefined,
            precompress: false,
            strict: true,
        }),
    },
}
