import { Injectable } from '@angular/core';

import { Observable, of } from 'rxjs';

import { __ENTITY_PASCAL__ } from './__ENTITY_KEBAB__';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';

export interface Response {
    result: __ENTITY_PASCAL__[];
    status: string;
    message: string;
};

@Injectable({
    providedIn: 'root'
})

export class __ENTITY_PASCAL__Service {

    constructor(private http: HttpClient) { }

    private apiUrl = '__ENTITY_URL__';

    private httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    }

    private log(message: string) {// console log for now
        console.log(message);
    }

    /**
     * Handle Http operation that failed.
     * Let the app continue.
     *
     * @param operation - name of the operation that failed
     * @param result - optional value to return as the observable result
     */
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

    serviceError: Response = {result: [], status: "error - network", message: ""}

    // Create __ENTITY_PASCAL__
    create(item: __ENTITY_PASCAL__): Observable<Response> {
        return this.http.post<Response>(this.apiUrl, item, this.httpOptions)
            .pipe(
                tap((response: Response) => this.log(`__ENTITY_PASCAL__.create(${response.status})`)),
                catchError(this.handleError<Response>('__ENTITY_PASCAL__.create()', this.serviceError))
            );
    }

    // Read __ENTITY_PASCAL__ collection
    read(): Observable<Response> {
        return this.http.get<Response>(this.apiUrl)
            .pipe(
                tap(_ => this.log('__ENTITY_PASCAL__.read()')),
                catchError(this.handleError<Response>('__ENTITY_PASCAL__.read()', this.serviceError))
            );
    }

    // Read __ENTITY_PASCAL__ by id
    find(__ENTITY_ID__: number): Observable<Response> {
        const url = `${this.apiUrl}/${__ENTITY_ID__}`;
        return this.http.get<Response>(url)
            .pipe(
                tap(_ => this.log(`__ENTITY_PASCAL__.find(${__ENTITY_ID__})`)),
                catchError(this.handleError<Response>(`__ENTITY_PASCAL__.find(${__ENTITY_ID__})`, this.serviceError))
            );
    }

    // Update __ENTITY_PASCAL__
    update(item: __ENTITY_PASCAL__): Observable<Response> {
        return this.http.put<Response>(this.apiUrl, item, this.httpOptions)
            .pipe(
                tap(_ => this.log(`__ENTITY_PASCAL__.update(${item.__ENTITY_ID__})`)),
                catchError(this.handleError<Response>(`__ENTITY_PASCAL__.update(${item.__ENTITY_ID__})`, this.serviceError))
            );
    }

    // Delete __ENTITY_PASCAL__
    delete(__ENTITY_ID__: number): Observable<Response> {
        const url = `${this.apiUrl}/${__ENTITY_ID__}`;
        return this.http.delete<Response>(url, this.httpOptions).pipe(
            tap(_ => this.log(`__ENTITY_PASCAL__.delete(${__ENTITY_ID__})`)),
            catchError(this.handleError<Response>(`__ENTITY_PASCAL__.delete(${__ENTITY_ID__})`, this.serviceError))
        );
    }
}
