module "repositories" {
    source = "./repositories"
}

module "lambdas" {
    source = "./lambdas"
    create_book_ecr_ui  = module.repositories.create_book_ecr_ui
    image_tag_lambda    = var.IMAGE_TAG
    find_book_ecr_ui    = module.repositories.find_book_ecr_ui
    find_book_ecr_arn   = module.repositories.find_book_ecr_arn
    delete_book_ecr_ui  = module.repositories.delete_book_ecr_ui
    update_book_ecr_ui  = module.repositories.update_book_ecr_ui
    get_book_ecr_ui     = module.repositories.get_book_ecr_ui
    get_book_ecr_arn    = module.repositories.get_book_ecr_arn
}