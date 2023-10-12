import adapter from "@sveltejs/adapter-node"
import { vitePreprocess } from "@sveltejs/kit/vite"

export default {
    kit: {
        adapter: adapter({
            out: "build",
            polyfill: false,
            precompress: false,
        }),
    },
    preprocess: vitePreprocess(),
}
