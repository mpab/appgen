import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatTableDataSource, MatTableModule } from '@angular/material/table';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatDialog } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

import { __ENTITY_PASCAL__FormComponent } from './__ENTITY_KEBAB__-form.component'
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
    columnNames: string[] = ["", "__KEY_PASCAL_SPACED_NO_ENUM__"];
    displayedColumns: string[] = ["__KEY_PASCAL_SPACED_NO_ENUM__"];

    __ENTITY_CAMEL__Collection: __ENTITY_PASCAL__Model[] = [];
    __ENTITY_CAMEL__CollectionCache: __ENTITY_PASCAL__Model[] = [];
    dataSource = new MatTableDataSource<__ENTITY_PASCAL__Model>([]);

    constructor(
            private alert: Alert,
            private dialog: MatDialog,
            private __ENTITY_CAMEL__Service: __ENTITY_PASCAL__Service,
        ) { }

    ngOnInit(): void {
        this.__ENTITY_CAMEL__Service.read()
            .subscribe(response =>
                this.handleResponse(response, () => {
                    this.__ENTITY_CAMEL__Collection = response.result;
                    this.cacheDataSource();
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

    onClickAdd() {
        let createItem = {
            entity: {
__ENTITY_INITIALIZER__
            }
        };

        const dialogRef = this.dialog.open(__ENTITY_PASCAL__FormComponent, {
            maxWidth: '100vw',
            maxHeight: '100vh',
            height: '30%',
            width: '40%',
            data: {
                item: createItem,
                columnNames: this.columnNames,
                crudMode: "Create",
                crudAction: "Save",
                hideDelete: true
            }
        });
        dialogRef.afterClosed().subscribe(result => {
            // clicking outside of the dialog returns undefined
            if (result === undefined || result === 'cancel') {
                this.restoreDataSource(); // revert any edits
                return;
            }

            if (result == 'action') {
                this.__ENTITY_CAMEL__Service.create(createItem.entity)
                    .subscribe(response => {
                        if (response.status === 'success') {
                            this.__ENTITY_CAMEL__Collection.push(response.result[0]);
                            this.cacheDataSource();
                            this.alert.success("added data");
                        } else {
                            // restore not required as no record created
                            this.alert.error(`could not add data: ${response.status}`);
                        }
                    });
            }
        });
    }

   onClickEdit(item: __ENTITY_PASCAL__Model) {
        let updateItem = {
            entity: item,
            constraints: {
            },
        };

        const dialogRef = this.dialog.open(__ENTITY_PASCAL__FormComponent, {
            maxWidth: '100vw',
            maxHeight: '100vh',
            height: '30%',
            width: '40%',
            data: {
                item: updateItem,
                columnNames: this.columnNames,
                crudMode: "Edit",
                crudAction: "Save"
            }
        });
        dialogRef.afterClosed().subscribe(result => {

            // clicking outside of the dialog returns undefined
            if (result === undefined || result === 'cancel') {
                this.restoreDataSource(); // revert any edits
                return;
            }

            if (result === 'delete') {
                this.__ENTITY_CAMEL__Service.delete(item.__ENTITY_SNAKE___id)
                    .subscribe(response => {
                        if (response.status === 'success') {
                            this.__ENTITY_CAMEL__Collection = this.__ENTITY_CAMEL__Collection.filter(i => i !== item);
                            this.cacheDataSource();
                            this.alert.success("deleted data");
                        } else {
                            this.restoreDataSource();
                            this.alert.error(`could not delete data: ${response.status}`);
                        }
                    });
            }

            if (result == 'action') {
                this.__ENTITY_CAMEL__Service.update(updateItem.entity)
                    .subscribe(response => {
                        if (response.status === 'success') {
                            this.cacheDataSource();
                            this.alert.success("saved data");
                        } else {
                            this.restoreDataSource();
                            this.alert.error(`could not save data: ${response.status}`);
                        }
                    });
            }
        });
    }

}
