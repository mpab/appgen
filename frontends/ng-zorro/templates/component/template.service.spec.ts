import { TestBed } from '@angular/core/testing';

import { INTERFACE_PASCALService } from './template.service';

describe('TemplateService', () => {
    let service: INTERFACE_PASCALService;

    beforeEach(() => {
        TestBed.configureTestingModule({});
        service = TestBed.inject(INTERFACE_PASCALService);
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });
});
