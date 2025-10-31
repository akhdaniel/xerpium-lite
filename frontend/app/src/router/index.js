import { createRouter, createWebHistory } from 'vue-router'
import MainMenu from '../components/MainMenu.vue'
import Dashboard from '../components/Dashboard.vue'

const routes = [
  {
    path: '/',
    name: 'MainMenu',
    component: MainMenu,
  },
  {
    path: '/:moduleName/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    props: true,
  },
  // Generic route for module-specific views
  {
    path: '/:moduleName/:modelName',
    name: 'ModelView',
    component: () => import('../components/GenericModelView.vue'), // Lazy load this component
    props: true,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
