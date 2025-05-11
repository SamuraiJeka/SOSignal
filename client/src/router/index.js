import { createRouter, createWebHistory } from 'vue-router/auto'
import MainPage from "@/pages/MainPage/MainPage.vue";


const routes = [
  {
    path: "/",
    component: () => import("../pages/MainPage/MainPage.vue")
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})


export default router
