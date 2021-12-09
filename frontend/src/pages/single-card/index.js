import { Container, Main, Button, TagsContainer, Icons, LinkComponent } from '../../components'
import { UserContext, AuthContext } from '../../contexts'
import { useContext, useState, useEffect } from 'react'
import styles from './styles.module.css'
import Ingredients from './ingredients'
import Description from './description'
import cn from 'classnames'
import { useRouteMatch, useParams, useHistory } from 'react-router-dom'
import MetaTags from 'react-meta-tags'

import { useRecipe } from '../../utils/index.js'
import api from '../../api'

const SingleCard = ({ loadItem, updateOrders }) => {
  const [ loading, setLoading ] = useState(true)
  const {
    recipe,
    setRecipe,
    handleLike,
    handleAddToCart,
    handleSubscribe
  } = useRecipe()
  const authContext = useContext(AuthContext)
  const userContext = useContext(UserContext)
  const { id } = useParams()
  const history = useHistory()

  useEffect(_ => {
    api.getRecipe ({
        recipe_id: id
      })
      .then(res => {
        setRecipe(res)
        setLoading(false)
      })
      .catch(err => {
        history.push('/recipes')
      })
  }, [])
  
  const { url } = useRouteMatch()
  const {
    author = {},
    image,
    tags,
    cooking_time,
    name,
    ingredients,
    text,
    is_favorited,
    is_in_shopping_cart
  } = recipe
  
  return <Main>
    <Container>
      <MetaTags>
        <title>{name}</title>
        <meta name="description" content={`Продуктовый помощник - ${name}`} />
        <meta property="og:title" content={name} />
      </MetaTags>
      <div className={styles['single-card']}>
        <img src={image} alt={name} className={styles["single-card__image"]} />
        <div className={styles["single-card__info"]}>
          <div className={styles["single-card__header-info"]}>
              <h1 className={styles["single-card__title"]}>{name}</h1>
              {authContext && <Button
                modifier='style_none'
                clickHandler={_ => {
                  handleLike({ id, toLike: !is_favorited })
                }}
              >
                {is_favorited ? <Icons.StarBigActiveIcon /> : <Icons.StarBigIcon />}
              </Button>}
          </div>
          <TagsContainer tags={tags} />
          <div>
            <p className={styles['single-card__text']}><Icons.ClockIcon /> {cooking_time} мин.</p>
            <p className={styles['single-card__text_with_link']}>
              <div className={styles['single-card__text']}>
                <Icons.UserIcon /> <LinkComponent
                  title={`${author.first_name} ${author.last_name}`}
                  href={`/user/${author.id}`}
                  className={styles['single-card__link']}
                />
              </div>
              {(userContext || {}).id === author.id && <LinkComponent
                href={`${url}/edit`}
                title='Редактировать рецепт'
                className={styles['single-card__edit']}
              />}
            </p>
          </div>
          <div className={styles['single-card__buttons']}>
            {authContext && <Button
              className={styles['single-card__button']}
              modifier='style_dark-blue'
              clickHandler={_ => {
                handleAddToCart({ id, toAdd: !is_in_shopping_cart, callback: updateOrders })
              }}
            >
              
            {is_in_shopping_cart ? <><Icons.DoneIcon color="#FFF"/>Рецепт добавлен</> : <><Icons.PlusIcon /> Добавить в покупки</>}
            </Button>}
            {(userContext || {}).id !== author.id && authContext && <Button
              className={styles['single-card__button']}
              clickHandler={_ => {
                handleSubscribe({ author_id: author.id, toSubscribe: !author.is_subscribed })
              }}
            >
              {author.is_subscribed ? 'Отписаться от автора' : 'Подписаться на автора'}
            </Button>}
          </div>
          <Ingredients ingredients={ingredients} />
          <Description description={text} />
        </div>
    </div>
    </Container>
  </Main>
}

export default SingleCard

