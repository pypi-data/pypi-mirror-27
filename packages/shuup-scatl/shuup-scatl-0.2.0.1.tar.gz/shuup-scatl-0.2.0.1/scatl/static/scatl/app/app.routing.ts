import {ModuleWithProviders} from '@angular/core'
import {Routes, RouterModule} from '@angular/router'

import {CatalogComponent} from 'app/catalog.comp'


export const routeLocation = {
    root: 'root',
    category: 'category',
}


const routes: Routes = [
    {
        // TODO allow to defined it with the plugin or admin config
        path: 'catalog',
        component: CatalogComponent,
        data: {
            location: routeLocation.root,
        },
    },
    // TODO: don't forget about 404 here
    {
        path: '**',
        component: CatalogComponent,
        data: {
            location: routeLocation.category,
        },
    },
]


export const routing: ModuleWithProviders = RouterModule.forRoot(routes)
