import { Injectable } from '@angular/core';

import { Observable, of } from 'rxjs';

import { __ENTITY_PASCAL__View } from './__ENTITY_KEBAB__.view';
import { __ENTITY_PASCAL__Model } from './__ENTITY_KEBAB__.model';
import { __ENTITY_PASCAL__ViewModel } from './__ENTITY_KEBAB__.viewmodel';
import { __ENTITY_PASCAL__ApiModel } from './__ENTITY_KEBAB__-api.model';

import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';

const API_UUID = "__API_UUID__";

export interface Response<T> {
    result: T;
    status: string;
    message: string;
};

type ResponseEntityModel = Response<__ENTITY_PASCAL__Model[]>;
type ResponseApiModel = Response<__ENTITY_PASCAL__ApiModel>;
let mvMapper = __ENTITY_PASCAL__ViewModel;

@Injectable({
    providedIn: 'root'
})

export class __ENTITY_PASCAL__ApiService {

    static createApiModel = (): __ENTITY_PASCAL__ApiModel => {
        return {
            version: {
                shape: '',
                major: 0,
                minor: 0,
                revision: 0
            },
            entities: [],
            views: [],
            entity_fields: [],
            references: {
__ENTITY_REFERENCES_DECLARATIONS__
            },
            _links: {
                "self": "",
                "next": "",
                "prev": "",
                "first": "",
                "last": ""
            },
            _paging: {
                entity_count: 0,
                page_size: 0,
                prev_cursor: 0,
                next_cursor: 0,
                first_cursor: 0,
                last_cursor: 0
            }
        };
    }
    public apiModel = __ENTITY_PASCAL__ApiService.createApiModel()

    constructor(private http: HttpClient) {
    }

    protected apiUrlBase = 'http://' + window.location.hostname + ':3000'
    protected apiStem = '/api/__ENTITY_PASCAL__';
    protected apiUrl = (query: string = '') => this.apiUrlBase + this.apiStem + query;
    protected linkUrl = (link: string) => this.apiUrlBase + link;

    private httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    }

    private log(message: string) {// console log for now
        console.log(message);
    }

    private handleError<T>(operation = 'operation', result?: T) {
        return (error: any): Observable<T> => {

            // TODO: send the error to remote logging infrastructure
            console.error(error); // log to console instead

            // TODO: better job of transforming error for user consumption
            this.log(`${operation} failed: ${error.message}`);

            // Let the app keep running by returning an empty result.
            return of(result as T);
        };
    }

    private modelError(message = "", result = []) {
        return {
            result: result,
            status: "error - network",
            message: message
        };
    }

    private apiModelError(message = "", result = __ENTITY_PASCAL__ApiService.createApiModel()) {
        return {
            result: result,
            status: "error - network",
            message: message
        };
    }

    /*
        Back-End-For-Front-End With Model View Mapping
    */

    readApiModel(): Observable<ResponseApiModel> {
        let fn = '__ENTITY_PASCAL__ApiService.readApiModel()';
        return this.http.get<ResponseApiModel>(this.apiUrl())
            .pipe(
                tap(response => {
                    this.log(`${fn} => ${response.status}`);
                    if (response.result) {
                        this.apiModel = response.result;
                        let expected = API_UUID.toLowerCase();
                        let api_shape = this.apiModel.version.shape.toLowerCase();
                        if (api_shape !== expected) throw (`api shape mismatch: expected: ${expected}, got: ${api_shape}`);

                        if (response.result.entities) {
                            let inflated_entities: __ENTITY_PASCAL__View[] = [];
                            this.apiModel.entities.forEach((e) => {
                                inflated_entities.push(mvMapper.mapModelToView(this.apiModel, e));
                            });
                            this.apiModel.views = inflated_entities;
                        }
                    }
                }),
                catchError(this.handleError<ResponseApiModel>(fn, this.apiModelError()))
            );
    }

    createEntity(view: __ENTITY_PASCAL__View): Observable<ResponseEntityModel> {
        let fn = '__ENTITY_PASCAL__ApiService.createEntity()';
        let model = mvMapper.mapViewToModel(this.apiModel, view);
        return this.http.post<ResponseEntityModel>(this.apiUrl(), model, this.httpOptions)
            .pipe(
                tap((response: ResponseEntityModel) => {
                    this.log(`${fn} => ${response.status}`);
                    if (response.status === 'success') {
                        this.apiModel.views.push(mvMapper.mapModelToView(this.apiModel, response.result[0]));
                        // TODO: get count from API
                        ++this.apiModel._paging.entity_count;
                    }
                }),
                catchError(this.handleError<ResponseEntityModel>(fn, this.modelError()))
            );
    }

    updateEntity(view: __ENTITY_PASCAL__View): Observable<ResponseEntityModel> {
        let fn = `__ENTITY_PASCAL__ApiService.updateEntity(${view.__ENTITY_SNAKE___id})`;
        let model = mvMapper.mapViewToModel(this.apiModel, view);
        return this.http.put<ResponseEntityModel>(this.apiUrl(), model, this.httpOptions)
            .pipe(
                tap(response => {
                    this.log(`${fn} => ${response.status}`);
                    if (response.status === 'success') {
                        const idx = this.apiModel.views.findIndex((o) => o.__ENTITY_ID__ === model.__ENTITY_ID__) ?? -1;
                        if (idx !== -1) {
                            this.apiModel.views.splice(idx, 1, mvMapper.mapModelToView(this.apiModel, response.result[0]));
                        }
                    }
                }),
                catchError(this.handleError<ResponseEntityModel>(fn, this.modelError()))
            );
    }

    deleteEntity(view: __ENTITY_PASCAL__View): Observable<ResponseEntityModel> {
        let fn = `__ENTITY_PASCAL__ApiService.deleteEntity(${view.__ENTITY_SNAKE___id})`;
        const url = `${this.apiUrl()}/${view.__ENTITY_ID__}`;
        return this.http.delete<ResponseEntityModel>(url, this.httpOptions).pipe(
            tap(response => {
                this.log(`${fn} => ${response.status}`);
                if (response.status === 'success') {
                    const idx = this.apiModel.views.findIndex((o) => o.__ENTITY_ID__ === view.__ENTITY_ID__) ?? -1;
                    if (idx !== -1) {
                        this.apiModel.views.splice(idx, 1);
                        // TODO: get count from API
                        --this.apiModel._paging.entity_count;
                    }
                }
            }),
            catchError(this.handleError<ResponseEntityModel>(fn, this.modelError()))
        );
    }

    /*
        Paging
    */

    readPage(fn: string, url: string) {
        return this.http.get<ResponseApiModel>(url)
            .pipe(
                tap(response => {
                    this.log(`${fn} => ${response.status}`);
                    if (response.result) {
                        let expected = API_UUID.toLowerCase();
                        let api_shape = response.result.version.shape.toLowerCase();
                        if (api_shape !== expected) throw (`api shape mismatch: expected: ${expected}, got: ${api_shape}`);
                        if (response.result.entities) {
                            this.apiModel.entities = response.result.entities
                            let inflated_entities: __ENTITY_PASCAL__View[] = [];
                            this.apiModel.entities.forEach((e) => {
                                inflated_entities.push(mvMapper.mapModelToView(this.apiModel, e));
                            });
                            this.apiModel.views = inflated_entities;
                            this.apiModel._links = response.result._links;
                            this.apiModel._paging = response.result._paging;
                        }
                    }
                }),
                catchError(this.handleError<ResponseApiModel>(fn, this.apiModelError()))
            );
    }

    nextPage(): Observable<ResponseApiModel> {
        return this.readPage('__ENTITY_PASCAL__ApiService.nextPage()', this.linkUrl(this.apiModel._links.next));
    }

    previousPage(): Observable<ResponseApiModel> {
        return this.readPage('__ENTITY_PASCAL__ApiService.previousPage()', this.linkUrl(this.apiModel._links.prev));
    }

    firstPage(): Observable<ResponseApiModel> {
        return this.readPage('__ENTITY_PASCAL__ApiService.firstPage()', this.linkUrl(this.apiModel._links.first));
    }

    lastPage(): Observable<ResponseApiModel> {
        return this.readPage('__ENTITY_PASCAL__ApiService.lastPage()', this.linkUrl(this.apiModel._links.last));
    }

    changePageSize(pageSize: number): Observable<ResponseApiModel> {
        return this.readPage('__ENTITY_PASCAL__ApiService.changePageSize()', this.apiUrl(`?page_size=${pageSize}`));
    }

}
