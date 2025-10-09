
# @app.get("/items", response_model=list[schemas.TMCOut])
# def list_items(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # items = db.query(models.TMC).all()

    # results = []
    # for item in items:
        # results.append({
            # "id": item.id,
            # "name": item.name,
            # "serial_number": item.serial_number,
            # "brand": item.brand,
            # "status": item.status.value if hasattr(item.status, "value") else item.status,
            # "responsible": item.responsible.username if item.responsible else None,
            # "location_id": item.location_id,
            # "location_name": item.location.name if item.location else None,
            # "comment": item.comment
        # })
    # return results

# @app.post("/items")
# def add_item(item: dict, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # new_item = InventoryItem(
        # name=item.get("name"),
        # serial_number=item.get("serial_number"),
        # brand=item.get("brand"),
        # status=item.get("status", StatusEnum.confirm),
        # responsible=item.get("responsible"),
        # location=item.get("location"),
        # location_id=item.get("location_id") #, LocationEnum.confirm)
    # )
    # db.add(new_item)
    # db.commit()
    # db.refresh(new_item)
    # return new_item

@app.put("/api/tmc/{tmc_id}/edit", response_model=schemas.TMCOut)
def edit_tmc_item(tmc_id: int, tmc_in: schemas.TMCUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = crud.update_tmc(db, tmc_id, tmc_in)
    if not obj:
        raise HTTPException(status_code=404, detail="TMC not found")
    return obj

@app.post("/api/tmc/{tmc_id}/transfer", response_model=schemas.TMCOut)
def transfer_tmc_item(tmc_id: int, new_responsible_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = crud.transfer_tmc(db, tmc_id, new_responsible_id)
    if not obj:
        raise HTTPException(status_code=404, detail="TMC not found")
    return obj

@app.post("/api/tmc/{tmc_id}/send_to_service", response_model=schemas.TMCOut)
def send_tmc_to_service(tmc_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = crud.send_to_service(db, tmc_id)
    if not obj:
        raise HTTPException(status_code=404, detail="TMC not found")
    return obj

@app.post("/api/tmc/{tmc_id}/return_from_service", response_model=schemas.TMCOut)
def return_tmc_from_service(tmc_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    obj = crud.return_from_service(db, tmc_id)
    if not obj:
        raise HTTPException(status_code=404, detail="TMC not found")
    return obj