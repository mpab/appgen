import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

import { __ENTITY_PASCAL__Model } from './__ENTITY_KEBAB__.model';
import { __ENTITY_PASCAL__Service } from './__ENTITY_KEBAB__.service';

import { Alert } from "../../components/alert.component/alert.component";

@Component({
    selector: 'app-__ENTITY_KEBAB__',
    imports: [
        FormsModule,
        MatTableModule,
        MatFormFieldModule,
        MatInputModule,
        MatButtonModule,
        MatIconModule,
        Alert,
    ],
    templateUrl: './__ENTITY_KEBAB__.component.html',
    styleUrl: './__ENTITY_KEBAB__.component.css'
})
export class __ENTITY_PASCAL__Component {
    columnNames: string[] = ["id", "__KEY__", "Action"];
    displayedColumns: string[] = ["id", "__KEY__", "Action"];

    __ENTITY_CAMEL__Collection: __ENTITY_PASCAL__Model[] = [];
    __ENTITY_CAMEL__CollectionCache: __ENTITY_PASCAL__Model[] = [];
    dataSource = new MatTableDataSource<__ENTITY_PASCAL__Model>([]);

    dirtyMap = new Map<number, boolean>();

    constructor(
        private alert: Alert,
        private __ENTITY_CAMEL__Service: __ENTITY_PASCAL__Service,
    ) { }

    ngOnInit(): void {
        this.__ENTITY_CAMEL__Service.read()
            .subscribe(response =>
                this.handleResponse(response, () => {
                    this.__ENTITY_CAMEL__Collection = response.result;
                    this.cacheDataSource();
                    this.dirtyMap.clear();
                })
            );
    }

    handleResponse(response: any, action: any) {
        if (response.status === 'success') {
            action();
            this.alert.success("read data");
        } else {
            this.alert.error(`could not read data: ${response.status}`);
        }
    }

    cacheDataSource(): void {
        this.__ENTITY_CAMEL__CollectionCache = [...this.__ENTITY_CAMEL__Collection].map((x) => ({ ...x }));
        this.dataSource = new MatTableDataSource(this.__ENTITY_CAMEL__Collection);
    }

    restoreDataSource(): void {
        this.__ENTITY_CAMEL__Collection = [...this.__ENTITY_CAMEL__CollectionCache].map((x) => ({ ...x }));
        this.dataSource = new MatTableDataSource(this.__ENTITY_CAMEL__Collection);
    }

    applyFilter(event: Event) {
        const filterValue = (event.target as HTMLInputElement).value;
        this.dataSource.filter = filterValue.trim().toLowerCase();
    }

    getNgModel(item: __ENTITY_PASCAL__Model): __ENTITY_PASCAL__Model {
        let boundItem = this.__ENTITY_CAMEL__Collection.find(
            (i) => i.__ENTITY_ID__ === item.__ENTITY_ID__);
        if (!boundItem) {
            boundItem = item;
            console.log("ERROR: getNgModel - !boundItem")
        }
        return boundItem;
    }

    onNgModelChange(event: Event, item: __ENTITY_PASCAL__Model) {
        let cachedItem = this.__ENTITY_CAMEL__CollectionCache.find(
            (i) => i.__ENTITY_ID__ === item.__ENTITY_ID__);
        if (!cachedItem) {
            cachedItem = item;
            console.log("ERROR: onNgModelChange - !cachedItem");
            return;
        }
        let realItem = this.__ENTITY_CAMEL__Collection.find(
            (i) => i.__ENTITY_ID__ === item.__ENTITY_ID__);
        if (!realItem) {
            realItem = item;
            console.log("ERROR: onNgModelChange - !realItem");
            return;
        }
        // TODO: compare/replace entire object
        realItem.__KEY__ = event.toString();
        if (realItem.__KEY__ === cachedItem.__KEY__) {
            this.dirtyMap.delete(realItem.__ENTITY_ID__);
        } else {
            this.dirtyMap.set(realItem.__ENTITY_ID__, true);
        }
    }

    disableSave(item: __ENTITY_PASCAL__Model): boolean {
        return !this.dirtyMap.has(item.__ENTITY_ID__);
    }

    onClickSave(item: __ENTITY_PASCAL__Model) {
        this.__ENTITY_CAMEL__Service.update(item)
            .subscribe(response => {
                if (response.status === 'success') {
                    this.cacheDataSource();
                    this.alert.success("saved data");
                    this.dirtyMap.delete(item.__ENTITY_ID__);
                } else {
                    this.restoreDataSource();
                    this.alert.error(`could not save data: ${response.status}`);
                }
            });
    }

}
