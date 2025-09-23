import {
  LayoutDashboard,
  ListTodo,
  Package,
  Users,
  MessagesSquare,
  Settings,
  UserCog,
  Wrench,
  Palette,
  Bell,
  Monitor,
  HelpCircle,
  LogOut,
  PiggyBank,
} from 'lucide-react'
// import { ClerkLogo } from '@/assets/clerk-logo'
import { type SidebarData } from '../types'

export const sidebarData: SidebarData = {
  user: {
    name: 'satnaing',
    email: 'satnaingdev@gmail.com',
    avatar: '/avatars/shadcn.jpg',
  },
  // teams: [
  //   {
  //     name: 'Shadcn Admin',
  //     logo: Command,
  //     plan: 'Vite + ShadcnUI',
  //   },
  //   {
  //     name: 'Acme Inc',
  //     logo: GalleryVerticalEnd,
  //     plan: 'Enterprise',
  //   },
  //   {
  //     name: 'Acme Corp.',
  //     logo: AudioWaveform,
  //     plan: 'Startup',
  //   },
  // ],
  teams: [],
  navGroups: [
    {
      title: 'General',
      items: [
        {
          title: 'Dashboard',
          url: '/',
          icon: LayoutDashboard,
        },
        {
          title: 'Transactions',
          url: '/tasks',
          icon: ListTodo,
        },
        {
          title: 'Budget Planning',
          url: '/budget',
          icon: PiggyBank,
        },
        {
          title: 'Analysis and Forecasting',
          url: '/users',
          icon: Users,
        },
        {
          title: 'Deals and Discounts',
          url: '/apps',
          icon: Package,
        },
        {
          title: 'AI Chatbot',
          url: '/chats',
          badge: '3',
          icon: MessagesSquare,
        },
        // {
        //   title: 'Secured by Clerk',
        //   icon: ClerkLogo,
        //   items: [
        //     {
        //       title: 'Sign In',
        //       url: '/clerk/sign-in',
        //     },
        //     {
        //       title: 'Sign Up',
        //       url: '/clerk/sign-up',
        //     },
        //     {
        //       title: 'User Management',
        //       url: '/clerk/user-management',
        //     },
        //   ],
        // },
      ],
    },
    {
      title: 'Other',
      items: [
        {
          title: 'Settings',
          icon: Settings,
          items: [
            {
              title: 'Profile',
              url: '/settings',
              icon: UserCog,
            },
            {
              title: 'Account',
              url: '/settings/account',
              icon: Wrench,
            },
            {
              title: 'Appearance',
              url: '/settings/appearance',
              icon: Palette,
            },
            {
              title: 'Notifications',
              url: '/settings/notifications',
              icon: Bell,
            },
            {
              title: 'Display',
              url: '/settings/display',
              icon: Monitor,
            },
          ],
        },
        {
          title: 'Help Center',
          url: '/help-center',
          icon: HelpCircle,
        },
        {
          title: 'Sign Out',
          url: '#',
          icon: LogOut,
        },
      ],
    },
  ],
}
