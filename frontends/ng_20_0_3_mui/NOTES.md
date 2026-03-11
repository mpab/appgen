# NG Tips

- Change table header and cell colors

Rule seems to be:  
mat-header-cell -> mat-mdc-header-row  
mat-cell -> mat-mdc-cell  

```css
.mat-mdc-header-row { background-color: lightblue; }
.mat-mdc-cell { background-color: whitesmoke; }
```

customise table

```css
.mat-mdc-header-row { background-color: whitesmoke; }

.x-mat-table {
    --mat-table-row-item-label-text-color: red; /* sets  first column color */
    --mat-table-row-item-outline-color: green;
    --mat-table-header-headline-color: blue;
    --mat-table-header-headline-weight: 600;
}
```

```html
<table mat-table [dataSource]="dataSource" multiTemplateDataRows class="x-mat-table">
---

- Change mat input background and font in a mat-cell

```css
.x-mat-mdc-text-field {
  --mdc-filled-text-field-container-color: white;
  --mat-form-field-container-text-size: 0.9rem;
}
```

```html
<td mat-cell class="x-mat-mdc-text-field" *matCellDef="let item">
```

---

- Change mat-button font size in a mat-cell

```css
.x-mat-mdc-button {
    --mdc-text-button-label-text-size: 0.9rem;
}
```

```html
<td mat-cell class="x-mat-mdc-button" *matCellDef="let item">
```

---

- hide hint field below mat-input in a mat-form-field when empty

```html
<mat-form-field subscriptSizing="dynamic">
```

## References

<https://danielk.tech/home/style-angular-material-table>  
<https://www.fusonic.net/en/blog/angular-material-customization>
