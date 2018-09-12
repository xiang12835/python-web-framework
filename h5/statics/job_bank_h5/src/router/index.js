import Vue from 'vue'
import Router from 'vue-router'
import Jobpage from '@/components/page/Jobpage'
import JobList from '@/components/page/JobList'
import JobInfo from '@/components/page/JobInfo'

import newspage from '@/components/page/newspage'
import newsInfo from '@/components/page/newsInfo'

import SearchInfo from '@/components/page/SearchInfo'
import SearchList from '@/components/page/SearchList'

import personPage from '@/components/page/personPage'
import myCollect from '@/components/page/myCollect'
import myNews from '@/components/page/myNews'
import myResume from '@/components/page/myResume'

import login from '@/components/page/login'

import remindpage from '@/components/page/remindpage'
import remindInfo from '@/components/page/remindInfo'

import prszactive from '@/components/activepage/prszactive'
import prszimg from '@/components/activepage/prszimg'


Vue.use(Router)

const routes = [
	{
		path: '/',
		component: Jobpage,	    
	},
	{
		path: '/newspage',
		name: 'newspage',
		component: newspage,
	},
	{
		path: '/jobList/:department_id',
		name: 'JobList',
		component: JobList,
	},
	{
		path: '/jobinfo/:job_id',
		name: 'JobInfo',
		component: JobInfo,
	},
	{
		path: '/newsinfo/:news_id',
		name: 'newsInfo',
		component: newsInfo,
	},
	{
		path: '/Searchlist',
		name: 'SearchList',
		component: SearchList,
	},
	{
		path: '/searchinfo/:searchname',
		name: 'SearchInfo',
		component: SearchInfo,
	},
	{
		path: '/mycollect',
		name: 'myCollect',
		component: myCollect,
	},
	{
		path: '/mynews',
		name: 'myNews',
		component: myNews,
	},
	{
		path: '/myresume',
		name: 'myResume',
		component: myResume,
	},
	{
		path: '/login',
		name: 'login',
		component: login,
	},
	{
		path: '/remindpage',
		name: 'remindpage',
		component: remindpage,
	},
	{
		path: '/remindnfo/:notice_id',
		name: 'remindInfo',
		component: remindInfo,
	},
	{
		path: '/personpage',
		name: 'personPage',
		component: personPage,
	},
	{
		path: '/prszactive',
		name: 'prszactive',
		component: prszactive,
	},
	{
		path: '/prszimg',
		name: 'prszimg',
		component: prszimg,
	}		
]

export default new Router({
  //mode: 'history',
  base: '/static/job_bank_h5/dist/',
  routes,
})
