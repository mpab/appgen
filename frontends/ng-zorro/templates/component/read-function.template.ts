__SERVICE_READ_FUNCTION__(): void {
    this.__SERVICE_NAME__.read()
        .subscribe(response => {
            if (response.status === 'success') {
                this.__COLLECTION_NAME__ = response.result
            }
        });
}
