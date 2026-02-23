import { Injectable } from '@angular/core';

import { Observable, of } from 'rxjs';

import { __ENTITY_PASCAL__View } from './__ENTITY_KEBAB__.view';
import { __ENTITY_PASCAL__Model } from './__ENTITY_KEBAB__.model';
import { __ENTITY_PASCAL__ViewModel } from './__ENTITY_KEBAB__.viewmodel';
import { __ENTITY_PASCAL__ApiModel } from './__ENTITY_KEBAB__-api.model';

import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';

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
            }
        };
    }
    public apiModel = __ENTITY_PASCAL__ApiService.createApiModel()

    constructor(private http: HttpClient) {
    }

    private apiUrl = '__API_URL__';

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
        return this.http.get<ResponseApiModel>(this.apiUrl)
            .pipe(
                tap(response => {
                    this.log(`${fn} => ${response.status}`);
                    this.apiModel = response.result;
                    if (response.result) {
                        this.apiModel = response.result;

                        let expected = 'BB9D0245-82F4-4E65-BD6E-D7A2A1694656'.toLowerCase();
                        let api_shape = this.apiModel.version.shape.toLowerCase();
                        if (api_shape !== expected) throw(`api shape mismatch: expected: ${expected}, got: ${api_shape}`);

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
        return this.http.post<ResponseEntityModel>(this.apiUrl, model, this.httpOptions)
            .pipe(
                tap((response: ResponseEntityModel) => {
                    this.log(`${fn} => ${response.status}`);
                    if (response.status === 'success') {
                        this.apiModel.views.push(mvMapper.mapModelToView(this.apiModel, response.result[0]));
                    }
                }),
                catchError(this.handleError<ResponseEntityModel>(fn, this.modelError()))
            );
    }

    updateEntity(view: __ENTITY_PASCAL__View): Observable<ResponseEntityModel> {
        let fn = `__ENTITY_PASCAL__ApiService.updateEntity(${view.__ENTITY_SNAKE___id})`;
        let model = mvMapper.mapViewToModel(this.apiModel, view);
        return this.http.put<ResponseEntityModel>(this.apiUrl, model, this.httpOptions)
            .pipe(
                tap(response => {
                    this.log(`${fn} => ${response.status}`);
                    if (response.status === 'success') {
                        const idx = this.apiModel.views.findIndex((o) => o.__ENTITY_SNAKE___id === model.__ENTITY_SNAKE___id) ?? -1;
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
        const url = `${this.apiUrl}/${view.__ENTITY_SNAKE___id}`;
        return this.http.delete<ResponseEntityModel>(url, this.httpOptions).pipe(
            tap(response => {
                this.log(`${fn} => ${response.status}`);
                if (response.status === 'success') {
                    const idx = this.apiModel.views.findIndex((o) => o.__ENTITY_SNAKE___id === view.__ENTITY_SNAKE___id) ?? -1;
                    if (idx !== -1) {
                        this.apiModel.views.splice(idx, 1);
                    }
                }
            }),
            catchError(this.handleError<ResponseEntityModel>(fn, this.modelError()))
        );
    }

}
