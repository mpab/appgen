# Set up and configure a frontend app

copy all ./src/app/app.component.* files to ./home/app.component.*

replace app.component.html

```html
<div><a routerLink="/home">Home</a></div>
<div><a routerLink="/the-new-component">The New Component</a></div>
<router-outlet></router-outlet>
```

app.routes.ts

```typescript
import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';

export const routes: Routes = [
    { path: '', pathMatch: 'full', redirectTo: '/home' }
  , { path: 'home', component: HomeComponent }
  , { path: 'business-process-evaluation-overview2', loadChildren: () => import('./the-new-component/the-new-component.routes').then(m => m.THE_NEW_COMPONENT_ROUTES) }
];
```

app.config.ts

```typescript
import { ApplicationConfig, provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http'; // add

import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [provideZoneChangeDetection({ eventCoalescing: true }), provideRouter(routes), provideHttpClient() /* add */]
};
```
