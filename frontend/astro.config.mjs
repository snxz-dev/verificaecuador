// @ts-check
import { defineConfig } from "astro/config";

// Sitio estático: la página llama a la API FastAPI desde el navegador.
export default defineConfig({
  output: "static",
});
