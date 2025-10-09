
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