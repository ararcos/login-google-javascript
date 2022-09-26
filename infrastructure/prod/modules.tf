module "repositories" {
    source = "./repositories"
}

module "lambdas" {
    source = "./lambdas"
    create_book_ecr_ui = module.repositories.create_book_ecr_ui
    image_tag_lambda = var.IMAGE_TAG
    find_book_ecr_ui = module.repositories.find_book_ecr_ui
    delete_book_ecr_ui = module.repositories.delete_book_ecr_ui
}