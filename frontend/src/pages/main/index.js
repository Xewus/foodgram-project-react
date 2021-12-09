import { Card, Title, Pagination, CardList, Container, Main, CheckboxGroup  } from '../../components'
import styles from './styles.module.css'
import { useRecipes } from '../../utils/index.js'
import { useEffect } from 'react'
import api from '../../api'
import MetaTags from 'react-meta-tags'

const HomePage = ({ updateOrders }) => {
  const {
    recipes,
    setRecipes,
    recipesCount,
    setRecipesCount,
    recipesPage,
    setRecipesPage,
    tagsValue,
    setTagsValue,
    handleTagsChange,
    handleLike,
    handleAddToCart
  } = useRecipes()

  
  const getRecipes = ({ page = 1, tags }) => {
    api
      .getRecipes({ page, tags })
      .then(res => {
        const { results, count } = res
        setRecipes(results)
        setRecipesCount(count)
      })
  }

  useEffect(_ => {
    getRecipes({ page: recipesPage, tags: tagsValue })
  }, [recipesPage, tagsValue])

  useEffect(_ => {
    api.getTags()
      .then(tags => {
        setTagsValue(tags.map(tag => ({ ...tag, value: true })))
      })
  }, [])


  return <Main>
    <Container>
      <MetaTags>
        <title>Рецепты</title>
        <meta name="description" content="Продуктовый помощник - Рецепты" />
        <meta property="og:title" content="Рецепты" />
      </MetaTags>
      <div className={styles.title}>
        <Title title='Рецепты' />
        <CheckboxGroup
          values={tagsValue}
          handleChange={handleTagsChange}
        />
      </div>
      <CardList>
        {recipes.map(card => <Card
          {...card}
          key={card.id}
          updateOrders={updateOrders}
          handleLike={handleLike}
          handleAddToCart={handleAddToCart}
        />)}
      </CardList>
      <Pagination
        count={recipesCount}
        limit={6}
        onPageChange={page => setRecipesPage(page)}
      />
    </Container>
  </Main>
}

export default HomePage

